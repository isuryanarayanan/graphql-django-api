"""
Utils for the accounts schema

MutationWrapper: A wrapper for mutations that handles errors and returns a message
QueryWrapper: A wrapper for queries that handles errors and returns a message
GraphqlErrorWrapper: A wrapper for graphql errors that handles errors and returns a message
"""

# Graphene imports
from typing import Dict
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError


# Mutation wrapper
class MutationWrapper(graphene.Mutation):
    message = graphene.String()
    status = graphene.Int()

    @classmethod
    def mutate(self, root, info, **kwargs):
        # Perform the mutation here
        result = self.perform_mutation(root, info, **kwargs)

        if result.status != 200:
            return GraphQLError(result.message)
        else:
            return self

    @classmethod
    def perform_mutation(self, root, info, **kwargs) -> Dict:
        """
        This method should be overridden by subclasses,
        to define their behavior
        """
        raise NotImplementedError(
            "You must override the `perform_mutation` method in the subclass.")


# Query wrapper
class QueryWrapper(graphene.ObjectType):
    message = graphene.String()
    status = graphene.Int()

    def resolve(self, info, **kwargs):
        try:
            return self.resolve_and_get_payload(info, **kwargs)
        except Exception as e:
            return QueryWrapper(message=str(e), status=400)


# Graphql error wrapper based on GraphQLError
class GraphqlErrorWrapper(GraphQLError):
    def __init__(self, message, status):
        super().__init__(message)
        self.status = status
        self.message = message

    def __str__(self):
        return self.message
