"""
Mutation to update a user's password, this is used in the accounts schema.
"""

# Graphene imports
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

# Django imports
from rest_framework_simplejwt.authentication import JWTAuthentication

# Local imports
from accounts.schema.types import BaseUserType as UserType
from accounts.models import User


# Mutation to update a user's password
class UpdatePassword(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        password = graphene.String(required=True)
        new_password = graphene.String(required=True)

    def mutate(self, info, password, new_password):
        # get authenticated user from the token inside the header
        user = JWTAuthentication().authenticate(info.context)[0]

        # Check if user is authenticated
        if not user.is_authenticated:
            return GraphQLError(
                "You must be logged in to update your password.")

        if user.check_password(password):
            user.set_password(new_password)
            user.save()
            return UpdatePassword(user=user)
        else:
            return GraphQLError("Incorrect password.")
