from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from base.connection import get_sparql_proxy, get_triple_store
from django.views.decorators.csrf import csrf_exempt
import tempfile

from models import RecentQuery

import settings

from base.rdf import CLIP, RDFS, abbreviate


#@login_required
def home(request):
    template_vars = RequestContext(request,{
        'sparql_endpoint' : settings.SPARQL_ENDPOINT_URL,
    })
    return render_to_response('rdfadmin/query.html', template_vars)


@csrf_exempt
def explore(request, file_hash):
    store = get_triple_store()
    data = request.GET.get("data", False)

    if data:
        store = get_triple_store()
        tf_data = tempfile.NamedTemporaryFile(dir=settings.VIRTUOSO_WORK_DIR)
        tf_data.write(data)
        tf_data.flush()
        store.load_file(tf_data.name, settings.DATA_GRAPH)

    sparql  = """
            prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT DISTINCT ?p ?pl ?o ?ol ?range WHERE {
                <%s> ?p ?o . 
                ?p rdfs:range ?range . 
                OPTIONAL { ?p <%s> ?pl }
                OPTIONAL { ?o <%s> ?ol }
            }
            ORDER BY ?p
            """ % (CLIP[file_hash],RDFS['label'], RDFS['label'])

    proxy = get_sparql_proxy()
    resource_data  = proxy.query(sparql,output='ResultSet')

    template_vars = RequestContext(request,{
        'sparql_endpoint' : settings.SPARQL_ENDPOINT_URL,
        'resource_data' : resource_data,
        'resource_uri' : abbreviate(CLIP[file_hash]),
    })
    return render_to_response('rdfadmin/explore.html', template_vars)


def proxy(request):
    query = request.GET['query']
    endpoint = request.GET.get('service_uri', settings.VIRTUOSO_ENDPOINT)
    if endpoint[:4] !=  "http":
        endpoint = "http://%s" % endpoint

    output = request.GET['output']

    context = request.GET.get('context','')
    user = None
    if hasattr(request, 'user'):
        user = request.user
        if not user.is_authenticated():
            user = None

    base = RecentQuery.objects
    lastQueries = base.filter(context='userInput').order_by('-creation')[:10]

    for q in lastQueries:
        if(q.query == query):
            q.delete()


    query_obj = RecentQuery(query = query, endpoint = endpoint, user = user, context = context)
    query_obj.save()

    proxy_obj = get_sparql_proxy();
    return HttpResponse(proxy_obj.query(query, endpoint, output, False))
