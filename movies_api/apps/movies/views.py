from typing import Dict, List

from django.conf import settings
from django.http import HttpRequest
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.views import extend_schema
from rest_framework import generics
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import QuerySet

from movies_api.apps.movies import serializers
from movies_api.apps.movies.data_provider_client import Client
from movies_api.apps.movies.data_provider_client.api.default import get_movies_movies_get
from movies_api.apps.movies.models import MovieRating
from movies_api.apps.movies.permissions import ManageOwnObjects
from movies_api.apps.movies.serializers import SearchMoviesResponseSerializer
from django.urls import reverse_lazy


class SearchMoviesAPIView(generics.ListAPIView):
    """
    Search movies that match search criteria.
    """

    permission_classes = (IsAuthenticated,)
    _external_data_provider_client = Client(base_url=settings.MOVIES_DATA_PROVIDER_BASE_URL)
    search_movies_url = reverse_lazy("ratings")

    @extend_schema(
        parameters=[
            OpenApiParameter(name="query", description="Query used to search for movies.", required=True, type=str),
            OpenApiParameter(name="page", description="Page number starting from 1.", type=int, default=1),
        ],
        description="Search movies endpoint.",
    )
    def get(self, request: HttpRequest, *args: List, **kwargs: Dict) -> Response:
        serializer = serializers.SearchMoviesRequestSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        queryset = self.get_queryset(serializer.validated_data)
        serializer = SearchMoviesResponseSerializer(instance=queryset)
        return Response(serializer.data)

    def get_queryset(self, query_params: Dict, *args: List, **kwargs: Dict) -> Dict:
        query = query_params.get("query", "")
        page_size = settings.REST_FRAMEWORK.get("PAGE_SIZE")
        page = query_params.get("page", 1)
        records_to_skip = (page - 1) * page_size
        paginated_movies = get_movies_movies_get.sync(
            client=self._external_data_provider_client, skip=records_to_skip, limit=page_size, query=query
        )
        if not paginated_movies:
            raise APIException("Data provider error")
        if page != 1 and len(paginated_movies.items) == 0:
            raise ValidationError({"detail": "Invalid page."})

        records_so_far = records_to_skip + len(paginated_movies.items)
        next_page_number = None if records_so_far >= paginated_movies.total else page + 1
        previous_page_number = None if page == 1 else page - 1
        data = {
            "count": paginated_movies.total,
            "next": self._get_url_for_page(next_page_number, query),
            "previous": self._get_url_for_page(previous_page_number, query),
            "results": paginated_movies.items,
        }
        return data

    def _get_url_for_page(self, page_number: int, query: str) -> str | None:
        if page_number is None:
            return None
        return self.request.build_absolute_uri(f"{self.search_movies_url}?page={page_number}&query={query}")


class CreateListMovieRatingAPIView(generics.ListCreateAPIView):
    """
    Creates and Lists movie ratings.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MovieRatingSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="rating_type",
                description="Either UPVOTE or DOWNVOTE. Leave it blank to get all ratings regardless of the type.",
                required=False,
                type=str,
            ),
        ],
        description="List movies voted by the logged in user.",
    )
    def get(self, request: HttpRequest, *args: List, **kwargs: Dict) -> Response:
        return self.list(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        serializer = serializers.ListRatingsRequestSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        queryset = MovieRating.objects.filter(user=self.request.user)
        rating_type = serializer.validated_data.get("rating_type")
        if rating_type:
            queryset = queryset.filter(rating_type=rating_type)
        return queryset

    def get_serializer(self, *args: List, **kwargs: Dict):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs["context"]["user"] = self.request.user
        return serializer_class(*args, **kwargs)

    def perform_create(self, serializer: serializers.MovieRatingSerializer) -> None:
        serializer.save(user=self.request.user)


class RetrieveUpdateDestroyMovieRatingAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Manages a movie rating.
    """

    queryset = MovieRating.objects.all()
    permission_classes = (IsAuthenticated, ManageOwnObjects)
    serializer_class = serializers.MovieRatingSerializer

    def get_serializer_class(self, *args: List, **kwargs: Dict):
        if self.request.method.upper() in ("PATCH", "PUT"):
            return serializers.MovieRatingUpdateSerializer
        return serializers.MovieRatingSerializer
