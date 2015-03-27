from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'MuellesObrero.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/', include('authentication.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('database.urls')),
    # url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index')
)
