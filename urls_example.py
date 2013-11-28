from django.conf.urls.defaults import patterns, url
from piston.resource import Resource
from piston.authentication import HttpBasicAuthentication
from nfe.oi.handlers import NFeHandler

auth = HttpBasicAuthentication(realm="ZinaRealm")
ad = {'authentication': auth}
nfe_resource = Resource(handler=NFeHandler, **ad)


urlpatterns = patterns('',
    url(r'^api/(?P<nfe_id>\d+)/$', nfe_resource, name='api_nfe'),
    url(r'^api/$', nfe_resource, name='api_nfe')
)
