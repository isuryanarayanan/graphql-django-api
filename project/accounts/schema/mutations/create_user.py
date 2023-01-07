"""
Mutation to create a new user, this is used in the accounts schema.
"""

# Graphene imports
import graphene
from graphene_django import DjangoObjectType

# Local imports
from accounts.schema.types import UserType
from accounts.models import User


# Mutation to create a new user
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        user = User(
            username=username,
            email=email,
            password=password,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)
