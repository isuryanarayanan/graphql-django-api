"""
Mutation to obtain and refresh access and refresh tokens, this is used in the accounts schema.
"""

# Django imports
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Graphene imports
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

# Local imports
from accounts.schema.types import BaseUserType as UserType
from accounts.models import User


# Mutation to obtain access and refresh tokens
class ObtainJSONWebToken(graphene.Mutation):
    user = graphene.Field(UserType)
    access_token = graphene.Field(graphene.String)
    refresh_token = graphene.Field(graphene.String)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = authenticate(info.context, email=email, password=password)
        if user is None:
            return GraphQLError('Invalid credentials')

        refresh = RefreshToken.for_user(user)
        return ObtainJSONWebToken(
            user=user,
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
            message='User logged in successfully',
            status=200
        )


# Mutation to refresh access and refresh tokens
class RefreshJSONWebToken(graphene.Mutation):
    user = graphene.Field(UserType)
    access_token = graphene.Field(graphene.String)
    refresh_token = graphene.Field(graphene.String)

    class Arguments:
        refresh_token = graphene.String(required=True)

    def mutate(self, info, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
        except Exception:
            return GraphQLError('Invalid refresh token')

        user = User.objects.get(id=refresh['user_id'])
        refresh = RefreshToken.for_user(user)
        return RefreshJSONWebToken(
            user=user,
            access_token=str(refresh.access_token),
            refresh_token=str(refresh),
            message='Token refreshed successfully',
            status=200
        )
