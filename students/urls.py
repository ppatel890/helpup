from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'students.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'helpup.views.home', name='home'),
    url(r'^register/$', 'helpup.views.register', name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^profile/$', 'helpup.views.profile', name='profile'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),
    url(r'^new_project/$', 'helpup.views.new_project', name='new_project'),
    url(r'^project_map/$', 'helpup.views.project_map', name='project_map'),
    url(r'^get_location/$', 'helpup.views.get_location', name='get_location'),
    url(r)
)
