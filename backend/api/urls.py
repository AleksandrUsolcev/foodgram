from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v10 = DefaultRouter()

v10.register('tags', views.TagViewSet, basename='tags')
v10.register('recipes', views.RecipeViewSet, basename='recipes')
v10.register('ingredients', views.IngredientViewSet, basename='ingredients')
v10.register(
    'users/subscribtions',
    views.UserSubscribeViewSet,
    basename='users_subscribe'
)

urlpatterns = [
    path('', include(v10.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
