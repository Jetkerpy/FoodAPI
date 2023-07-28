from backend.api.v1.product.serializers import (CategorySerializer,
                                                ProductSerializer)
from backend.api.v1.restaurant.serializers import (AddressSerializer,
                                                   RestaurantSerializer)
from backend.api.v1.viewsets.permissions import AdminDashboardPermission
from backend.product.models import Category, Ingredient, Product
from backend.restaurant.models import Address, Feedback, Media, Restaurant
from rest_framework import (filters, generics, permissions, response, status,
                            viewsets)
from rest_framework.decorators import action

from .serializers import (CategoryUpdateSerializer, CompanyMediaSerializer,
                          ProductUpdateSerializer, ReviewSerializer)


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


# ADDRESS API VIEWS
class AddressAPIViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [AdminDashboardPermission]

    def destroy(self, request, *args, **kwargs):
        """
            Bellow we gonna prevent to removing address
            if the is_default field is set to True
        """
        instance = self.get_object()
        if instance.is_default:
            return response.Response(
                {"message": "You can't remove the default address. So set default to another address."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
# END ADDRESS API VIEWS


# RESTAURANT API VIEWS
class RestaurantApiViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    

    @action(detail=False, methods='GET')
    def restaurant(self, request):
        restaurant = self.queryset.last()
        serializer = self.get_serializer(restaurant)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
# END RESTAURANT API VIEWS


# RESTAURANT MEDIA API VIEW
class RestaurantMediaApiViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = CompanyMediaSerializer
    http_method_names = ['post', 'put']
# END RESTAURANT MEDIA API VIEW