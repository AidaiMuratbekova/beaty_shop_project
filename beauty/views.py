from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from django.views.generic import CreateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, viewsets, status, filters
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product, Review, Like
from .permissions import IsAdminPermission
from .serializers import CategorySerializer, ProductSerializer,  ProductListSerializer, ReviewSerializer



class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['author', 'title']
    search_fields = ['title', 'created_at']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        print(self.action)
        if self.action == 'list':
            return ProductListSerializer
        return self.serializer_class


    @action(['GET', 'POST'], detail=True)
    def review(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        if request.method == 'GET':
            reviews = product.review.all()
            serializers = ReviewSerializer(reviews, many=True)
            return Response(serializers.data)
        elif request.method == 'POST':
            serializer = ReviewSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
        return Response(serializer.errors, status=404)

    @action(['POST'], detail=True)
    def like(self, request, slug=None):
        product = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(product=product, user=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'liked' if like.is_liked else 'dislike'
        except Like.DoesNotExist:
            Like.objects.create(product=product, user=user, is_liked=True)
        return Response(message, status=200)

    def get_permissions(self):
        """переопр данный метод"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permissions = [IsAdminPermission]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}






@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'products': reverse('product-list', request=request, format=format),
        'categories': reverse('categories-list', request=request, format=format),
    })


class ReviewCreateView(CreateView):
    queryset = Review.objects.none()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, ]
