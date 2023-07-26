import pytz
from backend.api.v1.product.serializers import IngredientSerializer
from backend.product.models import Category, Ingredient, Product
from backend.restaurant.models import Feedback
from django.core.files.storage import default_storage
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers


# CATEGORY UPDATE SERIALIZER 
class CategoryUpdateSerializer(serializers.ModelSerializer):
    """
        THIS ONLY WORK WHEN CATEGORY WILL BE UPDATED
        BEFORE UPDATING CHECKING VALUE :)
    """
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "is_active")
        read_only_fields = ("slug",)
        extra_kwargs = {
            "name": {'required': True},
            "image": {'required': False},
            "is_active": {'required': True}
        }


    def update(self, instance, validated_data):
        category_name = validated_data.get("name", instance.name).capitalize()
        new_image = validated_data.get("image", instance.image)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        if category_name != instance.name:
            self.__validate_category_name(category_name)
            ## EGER DE KIRITILIP ATIRG'AN NAME DI SAQLAMAY TURIP
            ## TEKSERIP ALADI, YAGNIY NAME SANNAN IBARAT EMESPE HAM
            ## OL NAME ALDIN SAQLANG'ANBA SONI QADAG'ALAP TURADI :)

        self.__delete_old_image(instance.image, new_image)
        ## DELETE OLD IMAGE YAGNIY TAZA IMAGE KIRITILIP ATIRSA OL
        ## GEZDE OLD IMAGE ULIWMAT OSHIRIP TASLAP ATIRMIZ MEDIA DAN OK 

        instance.name = category_name
        instance.image = new_image
        instance.save()
        return instance


    @classmethod
    def __validate_category_name(cls, value):
        if value.isdigit():
            raise serializers.ValidationError(f"sorry, your values '{value}' are digits so we can't save")
        
        name = value.capitalize()
        category = Category.objects.filter(name = name).exists()
        if category:
            raise serializers.ValidationError(f'{name} already exists, sorry :)')



    @classmethod
    def __delete_old_image(cls, old_image, new_image):
        if old_image and old_image != new_image:
            if default_storage.exists(old_image.path):
                default_storage.delete(old_image.path)
# END CATEGORY UPDATE SERIALIZER 


# PRODUCT UPDATE SERIALIZER
class ProductUpdateSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many = True)
    class Meta:
        model = Product
        fields = ("name", "slug", "description", "original_price", "image", "is_active", "ingredients")
    
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.original_price = validated_data.get("original_price", instance.original_price)
        instance.is_active = validated_data.get("is_active", instance.is_active)

        new_image = validated_data.get("image")
        if new_image:
            #DELETE OLD IMAGE IF NOT EQUAL NO_FOOD.WEBP
            if instance.image and instance.image.name != "product_images/no-food.webp":
                if default_storage.exists(instance.image.path):
                    default_storage.delete(instance.image.path)
            instance.image = new_image
        
        with transaction.atomic():
            instance.save()
            # UPDATE OR CREATE THE INGREDIENTS ASSOCIATED WITH THE PRODUCT
            for ingredient_data in ingredients_data:
                ingredient_name = ingredient_data.get("name").lower()
                ingredient, _ = Ingredient.objects.get_or_create(name = ingredient_name)
                
                instance.ingredients.add(ingredient)
            # REMOVE OLD INGREDIENTS
            current_ingredient_names = [ingredient_data.get("name").lower() for ingredient_data in ingredients_data]
            instance.ingredients.set(Ingredient.objects.filter(name__in = current_ingredient_names))
        return instance
# END PRODUCT UPDATE SERIALIZER


# REVIEW SERIALIZERS
class CustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    avatar = serializers.ImageField()


class ReviewSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    class Meta:
        model = Feedback
        fields = ('customer', 'rating', 'feedback', 'created_at')

    def to_representation(self, instance):
        tz = pytz.timezone("Asia/Tashkent")
        data = super().to_representation(instance)
        localized_time = timezone.localtime(instance.created_at, tz)
        created_at = localized_time.strftime("%d %B %Y %H:%M:%S")
        data['created_at'] = created_at
        return data
# END REVIEW SERIALIZERS





