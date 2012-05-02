from django.core.management.base import BaseCommand
from api.models import RDFResource
from base.connection import get_sparql_proxy

from base.rdf import RDFS, RDF

import settings

class Command(BaseCommand):
    help = 'Loads schema data from virtuoso triple store to the relational database.'
    args = '[graph_uri]'


    def handle(self, *args, **options):
        if len(args) > 0:
            graph = args[0]
        else:
            graph = settings.SCHEMA_GRAPH
            
        proxy = get_sparql_proxy()
        sparql = "SELECT DISTINCT ?res, ?label, ?type WHERE { ?res <%s> ?label . ?res <%s> ?type}" % (RDFS['label'], RDF['type'])

        resultSet = proxy.query(sparql,output='ResultSet')
        while resultSet.can_read():
            row = resultSet.get_row()
            RDFResource.objects.get_or_create(uri=row['res'].value, label=row['label'].value, type=row['type'].value)

