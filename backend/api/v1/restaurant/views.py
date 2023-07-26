from backend.restaurant.models import Address, Feedback, Media, Restaurant
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .serializers import (AddressSerializer, FeedBackSerializer,
                          RestaurantSerializer)


@api_view(['GET'])
def restaurant(request):
    """
        Restaurant API View
    """
    try:
        restaurant = Restaurant.objects.get()
        serializer = RestaurantSerializer(restaurant, many = False, context = {'request': request})
        return Response(
            {'restaurant': serializer.data},
            status=status.HTTP_200_OK
        )
    except Restaurant.DoesNotExist:
        return Response(
            {"error": "no restaurant found"},
            status=status.HTTP_404_NOT_FOUND
        )



@api_view(['GET'])
def addresses(request):
    addresses = Address.objects.all()
    if not addresses:
        return Response({"error": "no addresses found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = AddressSerializer(addresses, many = True)
    return Response(
        {"addresses": serializer.data},
        status=status.HTTP_200_OK
    )




@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def post_feedback(request):
    serializer = FeedBackSerializer(data=request.data, context={'request': request})
    if not serializer.is_valid(raise_exception=True):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save(customer=request.user)
    return Response("Feedback submitted successfully", status=status.HTTP_201_CREATED)
