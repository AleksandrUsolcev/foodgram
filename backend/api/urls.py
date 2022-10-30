from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v10 = DefaultRouter()

v10.register('users', views.UserViewSet, basename='users')
v10.register('tags', views.TagViewSet, basename='tags')
v10.register('recipes', views.RecipeViewSet, basename='recipes')
v10.register('subscriptions', views.SubscribeViewSet, basename='subscriptions')
v10.register('ingredients', views.IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(v10.urls))
]
