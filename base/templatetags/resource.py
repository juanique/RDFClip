from django import template
from django.template import Template, Context
import settings

register = template.Library()

class ResourceNode(template.Node):
    def __init__(self,row, res, label, property_column = False):
        self.row_variable = template.Variable(row)
        self.resource_column = res
        self.label_column = label
        self.property_column = property_column

    def render(self, context):
        row = self.row_variable.resolve(context)
        resource = row[self.resource_column]
    
        local_context = {}
        local_context['resource'] = resource.value
        local_context['label'] = row.get(self.label_column, resource).value
        if self.property_column:
            local_context['property'] = row[self.property_column].value

        anchor = """ <A title='{{resource}}' 
                        href='{{resource}}' 
                        {% if property %}
                            property='{{property}}'
                        {% endif %}
                     >
                        
                        {{label}}</A>
                """

        span = """<SPAN
                    {% if property %}
                        property='{{property}}'
                    {% endif %}
        
                >{{resource}}</SPAN>
               """

        template = Template(anchor if resource.type =='uri' else span)
        template = template.render(Context(local_context))

        return Template(template).render(context)


def resource_tag(parser, token):
    tokens = token.split_contents()
    (tag, row, uri, label) = tuple(tokens[:4])

    prop = False
    if len(tokens) > 4:
        prop = tokens[4]

    return ResourceNode(row, uri, label, prop)

register.tag('resource',resource_tag)
