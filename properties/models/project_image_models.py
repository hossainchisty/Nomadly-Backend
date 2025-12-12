from django.db import models

from base.models import BaseModel, DeepDeleteMixin
from cloudinary.models import CloudinaryField

class ProjectImage(BaseModel, DeepDeleteMixin):
    """ Project image model """
    image = CloudinaryField("project/images/visualization/")
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.description or "Unnamed Project Image"
