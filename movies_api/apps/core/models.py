from django.db import models
from django.utils.translation import gettext_lazy as _lazy


class BaseModel(models.Model):
    """
    Base model class.
    """

    created_at = models.DateTimeField(null=False, auto_now_add=True, editable=False, verbose_name=_lazy("Created at"))
    updated_at = models.DateTimeField(null=True, auto_now=True, editable=False, verbose_name=_lazy("Updated at"))

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f"{self.__class__.__name__} - {self.id}"
