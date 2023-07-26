from backend.api.v1.product.serializers import (CategorySerializer,
                                                ProductSerializer)
from backend.api.v1.viewsets.permissions import AdminDashboardPermission
from backend.product.models import Category, Ingredient, Product
from backend.restaurant.models import Feedback
from rest_framework import (filters, generics, permissions, response, status,
                            viewsets)
from rest_framework.decorators import action

from .serializers import (CategoryUpdateSerializer, ProductUpdateSerializer,
                          ReviewSerializer)


# CATEGORY API VIEW SIDE
class CategoryViewSet(viewsets.ModelViewSet):
    """
        CATEGORYVIEWSET INCLUDED METHODS LIST, RETRIEVE, CREATE,
        UPDATE, DELETE.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminDashboardPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = "slug"


    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return CategoryUpdateSerializer
        return CategorySerializer


    @action(detail=True, methods=['delete'])
    def perform_destroy(self, instance):
        """
            This is help us to remove image from MEDIA, when category object will be deleted
        """
        if instance.image:
            instance.image.delete()
        instance.delete()
        return response.Response(
            {'message': 'Object successfully deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )
# END CATEGORY API VIEW SIDE


# PRODUCT & INGREDIENTS API VIEW
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AdminDashboardPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category__name', 'ingredients__name', 'name']
    lookup_field = "slug"


    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProductUpdateSerializer
        return ProductSerializer


    @action(detail=True, methods=['delete'])
    def perform_destroy(self, instance):
        """
            This is help us to remove image from MEDIA, when product object will be deleted
        """
        if instance.image:
            if instance.image.name != "product_images/no-food.webp":
                instance.image.delete()
        instance.delete()
        return response.Response(
            {'message': 'Object successfully deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )
# END PRODUCT & INGREDIENTS API VIEW


# REVIEW API VIEWS
class ReviewAPiView(viewsets.ReadOnlyModelViewSet):
    """
        Review API View
    """
    queryset = Feedback.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AdminDashboardPermission]
# END REVIEW API VIEWS