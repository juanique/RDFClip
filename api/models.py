from django.db import models

# Create your models here.
class RDFTriple(models.Model):
    s = models.CharField(max_length = 200)
    p = models.CharField(max_length = 200)
    o = models.CharField(max_length = 200,blank=True,default='')
    action = models.CharField(max_length = 50)
    object_type = models.CharField(max_length = 32)
    timestamp = models.DateTimeField()

    def __str__(self):
        return "[%s]%s - %s %s %s" % (self.timestamp, self.action, self.s, self.p, self.o)

class RDFResource(models.Model):
    uri     = models.CharField(max_length = 200, db_index = True)
    label   = models.CharField(max_length = 200, db_index = True, null=True)
    type   = models.CharField(max_length = 200, db_index = True, null=True)

    def __str__(self):
        return self.label
