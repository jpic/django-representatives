# coding: utf-8

# This file is part of compotista.
#
# compotista is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or any later version.
#
# compotista is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Affero Public
# License along with django-representatives.
# If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) 2013 Laurent Peuch <cortex@worlddomination.be>
# Copyright (C) 2015 Arnaud Fabre <af@laquadrature.net>

import hashlib
from datetime import datetime

from django.db import models
from django.utils.functional import cached_property
from django.utils.encoding import smart_str, smart_unicode


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class HashableModel(models.Model):
    """
    An abstract base class model that provides a fingerprint
    field
    """
    
    fingerprint = models.CharField(
        max_length=40,
        unique=True,
    )

    class Meta:
        abstract = True

    def calculate_hash(self):
        fingerprint = hashlib.sha1()
        for field_name in self.hashable_fields:
            field = self._meta.get_field(field_name) 
            if field.is_relation:
                fingerprint.update(
                    getattr(self, field_name).fingerprint
                )
            else:
                fingerprint.update(
                    smart_str(getattr(self, field_name))
                )
        self.fingerprint = fingerprint.hexdigest()
        return self.fingerprint

    def get_hash_str(self):
        string = ''
        for field_name in self.hashable_fields:
            field = self._meta.get_field(field_name) 
            if field.is_relation:
                string += getattr(self, field_name).fingerprint
            else:
                string += smart_str(getattr(self, field_name))
        return string

    def save(self, *args, **kwargs):
        self.calculate_hash()
        super(HashableModel, self).save(*args, **kwargs)


class Country(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=2)

    @property
    def fingerprint(self):
        fingerprint = hashlib.sha1()
        fingerprint.update(smart_str(self.name))
        fingerprint.update(smart_str(self.code))
        return fingerprint.hexdigest()

    def __unicode__(self):
        return u'{} [{}]'.format(self.name, self.code)


class Representative(HashableModel, TimeStampedModel):
    """
    Base model for representatives
    """

    slug = models.SlugField(max_length=100)
    remote_id = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, default='')
    last_name = models.CharField(max_length=255, blank=True, default='')
    full_name = models.CharField(max_length=255)
    GENDER = (
        (0, "N/A"),
        (1, "F"),
        (2, "M"),
    )
    gender = models.SmallIntegerField(choices=GENDER, default=0)
    birth_place = models.CharField(max_length=255, blank=True, default='')
    birth_date = models.DateField(blank=True, null=True)
    cv = models.TextField(blank=True, default='')
    photo = models.CharField(max_length=512, null=True)
    active =  models.BooleanField(default=False)
    
    hashable_fields = ['remote_id']

    def __unicode__(self):
        return u'{} ({})'.format(smart_unicode(self.full_name), self.remote_id)

    def gender_as_str(self):
        genders = {0: 'N/A', 1: 'F', 2: 'M'}
        return genders[self.gender]

    class Meta:
        ordering = ['last_name', 'first_name']
        
# Contact related models
class Contact(TimeStampedModel):
    representative = models.ForeignKey(Representative)

    class Meta:
        abstract = True


class Email(Contact):
    email = models.EmailField()
    kind = models.CharField(max_length=255, blank=True, default='')


class WebSite(Contact):
    url = models.CharField(max_length=2048, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')


class Address(Contact):
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=255, blank=True, default='')
    street = models.CharField(max_length=255, blank=True, default='')
    number = models.CharField(max_length=255, blank=True, default='')
    postcode = models.CharField(max_length=255, blank=True, default='')
    floor = models.CharField(max_length=255, blank=True, default='')
    office_number = models.CharField(max_length=255, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')
    name = models.CharField(max_length=255, blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='') 


class Phone(Contact):
    number = models.CharField(max_length=255, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')
    address = models.ForeignKey(Address, null=True, related_name='phones')
    

class Group(HashableModel, TimeStampedModel):
    """
    An entity represented by a representative through a mandate
    """
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=10, blank=True, default='')
    kind = models.CharField(max_length=255, blank=True, default='')

    hashable_fields = ['name', 'abbreviation', 'kind']

    @cached_property
    def active(self):
        return self.mandates.filter(end_date__gte=datetime.now()).exists()

    def __unicode__(self):
        return unicode(self.name)


class Constituency(HashableModel, TimeStampedModel):
    """
    An authority for which a representative has a mandate
    """
    name = models.CharField(max_length=255)

    hashable_fields = ['name']

    @cached_property
    def active(self):
        return self.mandates.filter(end_date__gte=datetime.now()).exists()

    def __unicode__(self):
        return unicode(self.name)


class MandateManager(models.Manager):
    def get_queryset(self):
        return super(MandateManager, self).get_queryset().select_related('group', 'constituency')
    
class Mandate(HashableModel, TimeStampedModel):

    objects = MandateManager()
    
    group = models.ForeignKey(Group, null=True, related_name='mandates')
    constituency = models.ForeignKey(Constituency, null=True, related_name='mandates')
    representative = models.ForeignKey(Representative, related_name='mandates')
    role = models.CharField(
        max_length=25,
        blank=True,
        default='',
        help_text="Eg.: president of a political group at the European Parliament"
    )
    begin_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    link = models.URLField()

    hashable_fields = ['group', 'constituency', 'role',
                       'begin_date', 'end_date', 'representative']

    @property
    def active(self):
        return self.end_date >= datetime.now().date()

    def __unicode__(self):
        return u'Mandate : {representative},{role} {group} for {constituency}'.format(
            representative=self.representative,
            role=(u' {} of'.format(self.role) if self.role else u''),
            constituency=self.constituency,
            group=self.group
        )
