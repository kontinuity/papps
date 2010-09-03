from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from adserver.partner.models import Partner

attrs_dict = {'class': 'required'}

class SignupForm(forms.ModelForm):
  
  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
    
    order_these_first = [
      'username',
      'email',
      'password1',
      'password2',

      'first_name',
      'last_name',
    ]    
    
    for k in order_these_first:
      self.fields.keyOrder.remove(k)
      
    order_these_first.extend(self.fields.keyOrder)
    self.fields.keyOrder = order_these_first
    
    print self.fields.keyOrder
    
    # define fields order if needed

  
  username = forms.RegexField(regex=r'^\w+$',
                              max_length=30,
                              widget=forms.TextInput(attrs=attrs_dict),
                              label=_("Username"),
                              error_messages={'invalid': _("This value must contain only letters, numbers and underscores.")})
  email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
                           label=_("Email address"))
  password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label=_("Password"))
  password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                              label=_("Password (again)"))
  first_name = forms.CharField()
  last_name = forms.CharField()
  
  class Meta:
    model = Partner
    exclude = ('user',)  
        
  def clean_username(self):
      try:
          user = User.objects.get(username__iexact=self.cleaned_data['username'])
      except User.DoesNotExist:
          return self.cleaned_data['username']
      raise forms.ValidationError(_("A user with that username already exists."))

  def clean(self):
      if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
          if self.cleaned_data['password1'] != self.cleaned_data['password2']:
              raise forms.ValidationError(_("The two password fields didn't match."))
      return self.cleaned_data
