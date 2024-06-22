"""
Views for the recipe APIs
"""
from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Recipe,
    Tag,
    Ingredient,
    Coach,
    Supplement,
    Payment
   
      
     )
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for managing recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """return the serializer class for requests"""

        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """bass view set for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated users."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage Ingredients in the database"""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()


class CoachViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Coach objects."""
    queryset = Coach.objects.all()
    serializer_class = serializers.CoachSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    

    

class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Payment objects."""
    queryset = Payment.objects.all()
    serializer_class = serializers.PaymentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

   

    

class SupplementViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Supplement objects."""
    queryset = Supplement.objects.all()
    serializer_class = serializers.SupplementSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    

