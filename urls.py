from django.conf.urls import url
from django.contrib import admin
from .views import signin, signin_success, signup, signup_success


urlpatterns = [
     url(r'^signup$', signup, name='signup'),
     url(r'^contenta$', signin_success, name='signin_success'),
     url(r'^signin$', signin, name='signin'),
     url(r'^contentb$', signup_success, name='signup_success')

]