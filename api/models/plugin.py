import uuid
from django.db import models
from .server import Server

class Plugin(models.Model):

     def __str__(self) -> str:
          return self.name

     id = models.UUIDField( 
          primary_key = True, 
          default = uuid.uuid4, 
          editable = False) 
    
     name = models.CharField(max_length=256)
     #In schema will be stored the database schema that has to be created
     schema = models.JSONField()
     server = models.ForeignKey(Server, on_delete=models.RESTRICT, blank=True)
