from django.db import models
from adserver.partner.settings import *
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Partner(models.Model):
  company_name = models.CharField(max_length=255)
  company_type = models.PositiveIntegerField(choices=COMPANY_TYPE_CHOICES, default=COMPANY_TYPE_DEFAULT)
  company_type_other = models.CharField(max_length=255, blank=True, null=True)
  number_of_domains = models.PositiveIntegerField(blank=True, null=True)
  hosting_control_panel = models.PositiveIntegerField(choices=HOSTING_CONTROL_PANEL_CHOICES, default=HOSTING_CONTROL_PANEL_DEFAULT)
  hosting_control_panel_other = models.CharField(max_length=255, blank=True, null=True)
  webmail = models.PositiveIntegerField(choices=WEBMAIL_CHOICES, default=WEBMAIL_DEFAULT)
  number_of_users = models.PositiveIntegerField(blank=True, null=True)
  user = models.OneToOneField(User)
  
#def create_partner(sender, instance, created, **kwargs):  
#  if created:  
#    profile, created = Partner.objects.get_or_create(user=instance)
#
#post_save.connect(create_partner, sender=User)
