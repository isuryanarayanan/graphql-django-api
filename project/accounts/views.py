"""
This file contains the views for the accounts app.
"""

# Django imports
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Graphene imports
from graphene_django.views import GraphQLView
from accounts.schema.schema import schema


@csrf_exempt
def accounts_graphql_view(request):
    return GraphQLView.as_view(graphiql=True, schema=schema)(request)
