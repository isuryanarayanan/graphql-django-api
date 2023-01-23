"""
Mutation to create a new user, this is used in the accounts schema.
"""

# Graphene imports
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

# Local imports
from accounts.schema.types import BaseUserType
from accounts.models import User


class UserType(BaseUserType):
    class Meta:
        model = User
        exclude_fields = ('password',)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password):
        try:
            if User.objects.filter(username=username).exists():
                return GraphQLError('Username already exists')

            if User.objects.filter(email=email).exists():
                return GraphQLError('Email already exists')

            user = User.objects.create_email_user(
                username=username,
                email=email,
                password=password
            )
            user.save()

            return CreateUser(user=user, message='User created successfully', status=201)
        except Exception as e:
            return CreateUser(message=str(e), status=400)
