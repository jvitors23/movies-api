from typing import Dict

from rest_framework import serializers

from movies_api.apps.movies.models import MovieRating

from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


class SearchMoviesRequestSerializer(serializers.Serializer):
    query = serializers.CharField(required=True)
    page = serializers.IntegerField(min_value=1, default=1)


class SearchMoviesResponseItemSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    title = serializers.CharField()
    description = serializers.CharField()
    rating = serializers.FloatField()


class SearchMoviesResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField(min_value=0)
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = SearchMoviesResponseItemSerializer(many=True)


class MovieRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ("id", "rating_type", "movie_id", "user_id", "created_at", "updated_at")
        read_only_fields = ("id", "user_id", "created_at", "updated_at")

    def validate(self, attrs: Dict):
        movie_id = attrs.get("movie_id")
        existing_rating = MovieRating.objects.filter(movie_id=movie_id, user=self.context["request"].user).exists()
        if existing_rating:
            raise ValidationError(_("You can have only one rating per movie"))
        return super(MovieRatingSerializer, self).validate(attrs)


class MovieRatingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRating
        fields = ("id", "rating_type", "movie_id", "user_id", "created_at", "updated_at")
        read_only_fields = ("id", "movie_id", "user_id", "created_at", "updated_at")


class ListRatingsRequestSerializer(serializers.Serializer):

    rating_type = serializers.ChoiceField(
        choices=MovieRating.RatingType.choices,
        required=False,
    )
