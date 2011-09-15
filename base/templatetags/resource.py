from django import template
import settings

register = template.Library()

class ResourceNode(template.Node):
    def __init__(self,row, res, label):
        self.row_variable = template.Variable(row)
        self.resource_column = res
        self.label_column = label

    def render(self, context):
        row = self.row_variable.resolve(context)
        resource = row[self.resource_column]
        label = row.get(self.label_column, resource)

        if resource.type =='uri':
            return "<A title='%s' href='%s'>%s</A>" % (resource.value, resource.value, label.value)
        else:
            return "<SPAN>%s</SPAN>" % (resource.value)

def resource_tag(parser, token):
    tokens = token.split_contents()
    (tag, row, uri, label) = tuple(tokens[:4])

    return ResourceNode(row, uri, label)

register.tag('resource',resource_tag)
