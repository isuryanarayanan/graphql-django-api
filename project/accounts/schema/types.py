"""
Types for the accounts schema
"""

# Graphene imports
from graphene_django import DjangoObjectType

# Local imports
from accounts.models import User


# Graphql representation of the User model
class UserType(DjangoObjectType):
    class Meta:
        model = User
