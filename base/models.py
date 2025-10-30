from typing import Any

from django.db import models


class DeepDeleteMixin:
    """Mixin to handle deep deletion of related objects and files."""

    def remove_image_files(self, field):
        storage, path = field.storage, field.path
        storage.delete(path)

    def remove_m2m_objects(self, field):
        for obj in field.all():
            obj.delete()

    def delete(
        self, using: Any = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        fields = self.__class__._meta.get_fields()

        for field in fields:
            if isinstance(field, models.ImageField):
                field = getattr(self, field.name)
                try:
                    self.remove_image_files(field)
                except:
                    pass
            elif isinstance(field, models.ManyToManyField):
                field = getattr(self, field.name)
                self.remove_m2m_objects(field)

        return super().delete(using, keep_parents)


class BaseModel(DeepDeleteMixin, models.Model):
    """Base model with common fields."""

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
