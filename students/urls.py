from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

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
    url(r'^get_project/$', 'helpup.views.get_project', name='get_project'),
    url(r'^view_project/(?P<project_id>\w+)/$', 'helpup.views.view_project', name='view_project'),
    url(r'^get_user_project/$', 'helpup.views.get_user_project', name='get_user_project'),
    url(r'^form/$', 'helpup.views.form', name='form')

)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
