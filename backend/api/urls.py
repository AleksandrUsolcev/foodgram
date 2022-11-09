from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

v10 = DefaultRouter()

v10.register('tags', views.TagViewSet, basename='tags')
v10.register('recipes', views.RecipeViewSet, basename='recipes')
v10.register('ingredients', views.IngredientViewSet, basename='ingredients')
v10.register(
    'users/subscriptions',
    views.UserSubscribeViewSet,
    basename='users_subscribe'
)
v10.register(
    'users',
    views.UserSubscribeActionViewSet,
    basename='users_subscribe_action'
)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        views.CartDownloadView.as_view(),
        name='shopping_list_download'
    ),
    path('', include(v10.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
