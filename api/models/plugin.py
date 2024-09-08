import uuid
from django.db import models

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
