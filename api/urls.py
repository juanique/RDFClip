from django.conf.urls.defaults import *
import settings
import views 
from piston.resource import Resource
from api.handlers import RDFTripleHandler, ResourceHandler, ResourcePredicateHandler
from api.views import simple_handler_view

class CsrfExemptResource(Resource):
    def __init__(self, handler, authentication = None):
        super( CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

rdftriple_resource = CsrfExemptResource(RDFTripleHandler)

urlpatterns = patterns('',
    (r'^resource/(?P<file_hash>[0-9A-Za-z]+)/$', simple_handler_view(ResourceHandler)),
    (r'^resource/(?P<file_hash>[0-9A-Za-z]+)/(?P<predicate>[0-9A-Za-z]+:[0-9A-Za-z]+)', simple_handler_view(ResourcePredicateHandler)),
    (r'insert/',rdftriple_resource),
    (r'batch/',views.batch),
    (r'query/',views.query),
)
