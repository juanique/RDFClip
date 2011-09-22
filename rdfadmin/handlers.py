from piston.handler import BaseHandler
from piston.resource import Resource
import models


class SavedQueryHandler(BaseHandler):
    allowed_methods = ('GET','PUT','DELETE','POST')
    model = models.SavedQuery
    
    def read(self, request, *args, **kwargs):
        return self.model.objects.all()

    def create(self, request, *args, **kwargs):
        if request.content_type:
            data = request.data
            (query, created) = models.SavedQuery.objects.get_or_create (name=data['name'], endpoint=data.get('endpoint',''), query=data['query'], owner = request.user)

            if created:
                query.save()
                return query
            else:
                response = rc.DUPLICATE_ENTRY
                return response

class RecentQueryHandler(BaseHandler):
    allowed_methods = ('GET','PUT','DELETE','POST')
    model = models.RecentQuery

    def read(self, request):
        base = models.RecentQuery.objects
        return base.filter(context='userInput').order_by('-creation')[:10]

class CsrfExemptResource(Resource):
    def __init__(self, handler, authentication = None):
        super( CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

saved_query_resource = CsrfExemptResource(SavedQueryHandler)
recent_query_resource = CsrfExemptResource(RecentQueryHandler)
