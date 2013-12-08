from django.conf.urls import patterns, include, url

from django.contrib import admin
from tagger.views import *
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', welcome_page),
    url(r'^mark_person/(?P<face_id>\d+)/+$', mark_person_page, name='tagger.mark_person_page'),
    url(r'^admin/', include(admin.site.urls)),
)
