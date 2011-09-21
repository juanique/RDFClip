import settings

from piston.handler import BaseHandler
from models import RDFTriple
from base.connection import get_sparql_proxy

from base.rdf import abbreviate, CLIP, RDFS

import triplestore


class RDFTripleHandler(BaseHandler):
    allowed_methods = ('POST')
    model = RDFTriple

    def create(self, request, *args, **kwargs):
        if request.content_type:
            triplestore.insert(data)


class SimpleHandler:

    def handle_request(self, request, *args, **kwargs):
        method = request.META['REQUEST_METHOD']

        if method not in self.allowed_methods:
            raise

        if method == 'POST':
            return self.create(request,  **kwargs)
        if method == 'GET':
            return self.read(request,  **kwargs)

class ResourceHandler(SimpleHandler):
    allowed_methods = ('POST', 'GET')

    def read(self, request, file_hash):
        sparql  = """
                SELECT DISTINCT ?predicate ?object ?range WHERE {
                    <%s> ?predicate ?object . 
                    ?predicate rdfs:range ?range . 
                }
                ORDER BY ?p
                """ % CLIP[file_hash]

        proxy = get_sparql_proxy()
        resource_data  = proxy.query(sparql,output='ResultSet')

        output = {}

        for row in resource_data:
            obj = abbreviate(row['object'].value) if row['object'].type =='uri' else row['object'].value
            ran = abbreviate(row['range'].value)
            pred = abbreviate(row['predicate'].value)
            output[pred] = { 'value' : obj, 'type' : ran }

        return output

class ResourcePredicateHandler(SimpleHandler):
    allowed_methods = ('POST', 'GET')

    def read(self, request, file_hash, predicate):
        sparql  = """
                SELECT DISTINCT ?object ?object_prop ?object_range ?label ?object_value
                WHERE {
                    <%s> %s ?object . 
                    OPTIONAL {?object ?object_prop ?object_value }
                    OPTIONAL {?object_prop rdfs:range ?object_range }
                    OPTIONAL { ?object rdfs:label ?object_label }
                }
                ORDER BY ?p
                """ % (CLIP[file_hash], predicate)

        proxy = get_sparql_proxy()
        resource_data  = proxy.query(sparql,output='ResultSet')

        output = []
        aggregated = {}

        for row in resource_data:
            obj = row['object']
            if obj.type == 'uri':
                ran = abbreviate(row['object_range'].value)
                prop = abbreviate(row['object_prop'].value)

                obj_val = row['object_value']
                value = abbreviate(obj_val.value) if obj_val.type == 'uri' else obj_val.value

                try:
                    aggregated[obj.value][prop] = value
                except KeyError:
                    aggregated[obj.value] = {}
                    aggregated[obj.value][prop] = value
            else:
                output.append(obj.value)

        for (key, val) in aggregated.items():
            output.append(val)
        return output
