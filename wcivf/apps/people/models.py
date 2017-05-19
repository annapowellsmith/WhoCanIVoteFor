from django.db import models
from django.core.urlresolvers import reverse
from django.utils.text import slugify

from wcivf import settings

from elections.models import Election, Post
from parties.models import Party

from .managers import PersonPostManager, PersonManager


class PersonPost(models.Model):
    person = models.ForeignKey('Person')
    post = models.ForeignKey(Post)
    party = models.ForeignKey(Party, null=True)
    election = models.ForeignKey(Election, null=False)
    list_position = models.IntegerField(blank=True, null=True)
    objects = PersonPostManager()

    def __str__(self):
        return "{} ({}, {})".format(
            self.person.name,
            self.post.label,
            self.election.slug
        )

    class Meta:
        ordering = ('-election__election_date', )
        unique_together = ('person', 'post', 'election')



class Person(models.Model):
    ynr_id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(blank=True, max_length=255)
    email = models.EmailField(null=True)
    gender = models.CharField(blank=True, max_length=255, null=True)
    birth_date = models.CharField(null=True, max_length=255)
    photo_url = models.URLField(blank=True, null=True)

    # contact points
    twitter_username = models.CharField(blank=True, null=True, max_length=100)
    facebook_page_url = models.CharField(blank=True, null=True, max_length=800)
    facebook_personal_url = models.CharField(blank=True, null=True, max_length=800)
    linkedin_url = models.CharField(blank=True, null=True, max_length=800)
    homepage_url = models.CharField(blank=True, null=True, max_length=800)

    #Bios
    wikipedia_url = models.CharField(blank=True, null=True, max_length=800)
    wikipedia_bio = models.TextField(null=True)
    statement_to_voters = models.TextField(null=True)

    objects = PersonManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('person_view', args=[
                str(self.ynr_id),
                slugify(self.name)
            ])

    def get_ynr_url(self):
        return "{}/person/{}/".format(settings.YNR_BASE, self.ynr_id)

    @property
    def should_show_email_cta(self):
        show_cta = bool(self.email)

        conditions = [
            self.statement_to_voters,
        ]

        all_conditions = not any(map(bool, conditions))

        return all([show_cta, all_conditions])


class AssociatedCompany(models.Model):
    person              = models.ForeignKey(Person)
    company_name        = models.CharField(max_length=255)
    company_number      = models.CharField(max_length=50)
    company_status      = models.CharField(max_length=50)
    role                = models.CharField(max_length=50)
    role_status         = models.CharField(max_length=50, blank=True, null=True)
    role_appointed_date = models.DateField()
    role_resigned_date  = models.DateField(blank=True, null=True)
