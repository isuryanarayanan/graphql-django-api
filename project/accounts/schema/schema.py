"""
Schema for the accounts app
"""

# Graphene imports
import graphene

# Schema imports

# Mutations
from accounts.schema.mutations.create_user import CreateUser
from accounts.schema.mutations.update_password import UpdatePassword
from accounts.schema.mutations.tokens import ObtainJSONWebToken, RefreshJSONWebToken

# Queries
from accounts.schema.queries.fetch_users import fetchUsers


class Query(fetchUsers):
    """
    All the queries for the accounts app need to be added here as a parameter.
    """
    pass


class Mutation(graphene.ObjectType):
    """
    All the mutations for the accounts app need to be added here as a field.
    """
    create_user = CreateUser.Field()
    password_update = UpdatePassword.Field()
    obtain_token = ObtainJSONWebToken.Field()
    refresh_token = RefreshJSONWebToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
