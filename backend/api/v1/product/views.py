from backend.product.models import Category, Ingredient, Product
from rest_framework import generics, response, status

from .serializers import CategorySerializer, ProductSerializer


# CLIENT WEB API
class CategoryListApiView(generics.ListAPIView):
    """
        CATEGORY LIST API VIEW FOR CLIENT APP 
        RETURN QUERYSET OF CATEGORY IS_ACTIVE = TRUE
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(is_active = True)
        return queryset



class ProductListApiView(generics.ListAPIView):
    """
        Product List Api View for client app
        return queryset of product if is_active = True
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(is_active = True)
        return queryset


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        #print(queryset.query)
        category = request.query_params.get("category") or None
        if category is not None:
            queryset = queryset.filter(category__slug = category)

            if not queryset.exists():
                return response.Response(
                    {'message': 'No products found for the specified category.'},
                    status=status.HTTP_404_NOT_FOUND
                )
         
        serializer = self.get_serializer(queryset, many = True)
        return response.Response(serializer.data)