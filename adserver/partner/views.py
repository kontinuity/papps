from django.shortcuts import render_to_response
from django.template.context import RequestContext
from adserver.partner.forms import SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.forms.util import ErrorDict

def home(request):
  
  print request.user.is_authenticated()
  if (request.user.is_authenticated()):
    print 'Auth'
    return render_to_response('partner/dashboard.html', {}, context_instance=RequestContext(request))
  
  form = AuthenticationForm()
  return render_to_response('partner/home.html', {'form': form}, context_instance=RequestContext(request))

def signup(request):
  if (request.user.is_authenticated()):
    return render_to_response('partner/dashboard.html', {}, context_instance=RequestContext(request))
  
  if request.POST:
    form = SignupForm(request.POST)
    if form.is_valid():
      #TODO: Avoid save (create_user) and update (is_active) 
      user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
      user.is_active = False;
      user.save()
      partner = form.save(commit=False)
      partner.user = user
      partner.save()
      logout(request)
      return render_to_response('partner/signup_complete.html')
  else:
    form = SignupForm()
  
  return render_to_response('partner/signup.html', {'form': form}, context_instance=RequestContext(request))

@csrf_protect
@never_cache
def login_user(request, template_name='registration/login.html',
          redirect_field_name='next',
          authentication_form=AuthenticationForm):

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            # Heavier security check -- redirects to http://example.com should 
            # not be allowed, but things like /view/?param=http://example.com 
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL
            
            # Okay, security checks complete. Log the user in.
            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)

    else:
        form = authentication_form(request)
    
    request.session.set_test_cookie()
    
    inactive = False
    if form.get_user() and not form.get_user().is_active:
      inactive = True
      form._errors = ErrorDict()
    
    return render_to_response(template_name, {
        'form': form,
        'inactive': inactive,
        redirect_field_name: redirect_to,
    }, context_instance=RequestContext(request))

