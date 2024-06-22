"""
Url mapping for the Recipe app.
"""
from django.urls import (
    path,
    include,
    )

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('coaches', views.CoachViewSet)
router.register('payments', views.PaymentViewSet)
router.register('supplements', views.SupplementViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
