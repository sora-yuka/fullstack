from rest_framework import serializers
from applications.feedback.models import Comment, Favourite
from applications.feedback.serializers import CommentSerializer, FavouriteSerializer
from applications.product.models import Product, Image
from django.db.models import Avg


class ImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)
    file_image = ImageSerializer(many=True, read_only=True)
    discount = serializers.IntegerField(max_value=100)

    
    class Meta:
        model = Product
        fields = '__all__'
        
       
    def create(self, validated_data):
        request = self.context.get('request')
        product = Product.objects.create(**validated_data)
        files = request.FILES
        list_images = []
        
        for image in files.getlist('images'):
            list_images.append(Image(product=product, image=image))
        Image.objects.bulk_create(list_images)
        return product
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        comment = Comment.objects.filter(product=instance.id)
        serializer = CommentSerializer(comment, many=True)
        comments = serializer.data
        
        rep['price'] = float(instance.price) - float(instance.discount/100)*float(instance.price)
        rep['likes'] = instance.likes.filter(like=True).count()
        rep['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']
        rep['comment'] = comments
        return rep
    