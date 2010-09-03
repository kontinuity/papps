from django.contrib import admin
from adserver.partner.models import Partner
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class PartnerInline(admin.StackedInline):
  model = Partner

class PartnerAdmin(admin.ModelAdmin):
  
  inlines = [PartnerInline]
  list_display = ('username', 'email', 'is_active', 'is_superuser')
  fieldsets = (
    (None, {'fields': ('username',)}),
    (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
    (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    (_('Audit info'), {'fields': ('last_login', 'date_joined')}),
  )
  exclude = ['user_permissions', 'password', 'groups']
  
admin.site.unregister(User)
admin.site.register(User, PartnerAdmin)
