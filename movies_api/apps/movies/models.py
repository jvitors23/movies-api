from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from movies_api.apps.core.models import BaseModel


class MovieRating(BaseModel):
    """
    Movie Rating model
    """

    class RatingType(models.TextChoices):
        UPVOTE = "UPVOTE", _("Upvote")
        DOWNVOTE = "DOWNVOTE", _("Downvote")

    movie_id = models.UUIDField(null=False, blank=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating_type = models.CharField(max_length=8, choices=RatingType.choices, default=RatingType.UPVOTE)

    class Meta:
        app_label = "movies"
        constraints = [models.UniqueConstraint(fields=["movie_id", "user"], name="unique rating")]
