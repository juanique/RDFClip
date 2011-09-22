from django.views.decorators.csrf import csrf_exempt
from base.decorators import json_view
from django.views.decorators.http import require_http_methods

class SimpleHandler:
    def handle_request(self, request, *args, **kwargs):
        method = request.META['REQUEST_METHOD']

        if method not in self.allowed_methods:
            raise

        if method == 'POST':
            return self.create(request,  **kwargs)
        if method == 'GET':
            return self.read(request,  **kwargs)

def simple_handler_view(handler_class):
    handler = handler_class()
    methods_decorator = require_http_methods(list(handler.allowed_methods))

    def output_view(request, *args, **kwargs):
        return handler.handle_request(request, *args, **kwargs)

    return methods_decorator(csrf_exempt(json_view(output_view)))
