# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from base.decorators import json_view
from django.template import Template
import triplestore
from base.connection import get_sparql_proxy

@csrf_exempt
@json_view
def batch(request,data):
    triplestore.insert(data.get('insert',[]))
    triplestore.delete(data.get('delete',[]))
    
@csrf_exempt
@json_view
def query(request,data):
    pred= data['pred']
    obj= data['obj']
    proxy = get_sparql_proxy()

    pred_resource = RDFResource.objects.filter(label=pred)
    pred = pred_resource[0].uri

    sparql_template = TEMPLATE("""
             SELECT ?sub, ?label, ?size
             FROM <{{graph}}> 
             WHERE {
                ?sub <{{pred}}> <{{obj}}> .
                ?sub <{{nie:byteSize}}> ?size .
                OPTIONAL { ?sub <{{rdfs:label}}> ?label . }
            }
            """)

    context = {
            'graph' : settings.DATA_GRAPH,
            'pred'  : pred,
            'nie:byteSize' : NIE['bytesize'],
            'rdfs:label' : RDFS['label'],
            }


    return proxy.query(sparql_template.render(context),output='json')

def simple_handler_view(handler_class):
    handler = handler_class()
    methods_decorator = require_http_methods(list(handler.allowed_methods))

    def output_view(request, *args, **kwargs):
        return handler.handle_request(request, *args, **kwargs)

    return methods_decorator(csrf_exempt(json_view(output_view)))


