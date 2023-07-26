from backend.restaurant.models import Address, Feedback, Media, Restaurant
from rest_framework import serializers


class MediaSerializer(serializers.ModelSerializer):
    """
        Restaurant Media Images Serializer ok :)
    """
    class Meta:
        model = Media
        fields = ("image", "alt_text", "is_feature")



class RestaurantSerializer(serializers.ModelSerializer):
    """
        Restaurant Serializer :)
    """
    qr_code = serializers.SerializerMethodField()
    restaurant_images = MediaSerializer(many = True)
    class Meta:
        model = Restaurant
        fields = ("name", "slug", "about_us", "phone_number1", "phone_number2", "telegram_link", "instagram_link", "facebook_link", "qr_code", "created_at", "updated_at", "restaurant_images")

    
    def get_qr_code(self, obj):
        request = self.context.get("request")
        if obj.qr_code:
            return request.build_absolute_uri(obj.qr_code.url)
        return None



class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"



class FeedBackSerializer(serializers.ModelSerializer):
    restaurant = serializers.SlugRelatedField(
        slug_field="slug",
        queryset = Restaurant.objects.all()
    )
    class Meta:
        model = Feedback
        fields = ("restaurant", "rating", "feedback")


    def validate(self, data):
        user = self.context['request'].user
        restaurant = data.get("restaurant")
        existing_restaurant = Feedback.objects.filter(customer=user, restaurant=restaurant).exists()
        if existing_restaurant:
            raise serializers.ValidationError("You have already submitted a rating for this restaurant.")
        return data
