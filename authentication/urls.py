from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	url(r'login/$', 'authentication.views.signin', name='signin'),
	url(r'logout/$', 'authentication.views.signout', name='signout'),
	url(r'users/$', 'authentication.views.users', name='users'),
	url(r'password/$', 'authentication.views.update_pass', name='update_pass'),
)