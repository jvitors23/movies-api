from typing import Dict

from rest_framework import serializers

from movies_api.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects"""

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )
        read_only_fields = ("id",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data: Dict) -> User:
        """Create a new user with encrypted password and return it"""
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: Dict) -> User:
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
