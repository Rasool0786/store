from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from . import serializers, models
from .paginations import DefaultPagination
from .permissions import IsAdminUserOrReadOnly, SendPrivateEmailToCustomerPermission
from .signals import order_created


class ProductViewSet(ModelViewSet):
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    # filterset_class = ProductFilter
    # filterset_fields = ["category_id", "inventory"]
    ordering_fields = ["name", "unit_price", "inventory"]
    pagination_class = DefaultPagination
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = models.Product.objects.all()
    search_fields = ["name", "category__title"]
    serializer_class = serializers.ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, pk):
        product = get_object_or_404(
            models.Product.objects.select_related("category"), pk=pk
        )
        if product.order_items.count() > 0:
            return Response(
                {
                    "error": "There is some order items including this product. Please remove them first."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminUserOrReadOnly]
    queryset = models.Category.objects.all().annotate(products_count=Count("products"))
    serializer_class = serializers.CategorySerializer

    def destroy(self, request, pk):
        category = get_object_or_404(
            models.Category.objects.annotate(
                products_count=Count("products"),
            ),
            pk=pk,
        )
        if category.products.count() > 0:
            return Response(
                {
                    "error": "There is some products including this category. Please remove them first."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        product_pk = self.kwargs["product_pk"]
        return (
            models.Comment.objects.filter(product_id=product_pk)
            .all()
            .select_related("comments")
        )

    def get_serializer_context(self):
        return {"product_pk": self.kwargs["product_pk"]}


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "options", "head"]

    def get_queryset(self):
        cart_pk = self.kwargs["cart_pk"]
        return (
            models.CartItem.objects.filter(cart_id=cart_pk)
            .all()
            .select_related("product")
        )

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.AddCartItemSerializer
        elif self.request.method == "PATCH":
            return serializers.UpdateCartItemSerializer
        return serializers.CartItemSerializer

    def get_serializer_context(self):
        return {"cart_pk": self.kwargs["cart_pk"]}


class CartViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    lookup_value_regex = "[0-9a-fA-F]{8}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{12}"
    queryset = models.Cart.objects.all().prefetch_related("items__product")
    serializer_class = serializers.CartSerializer


class CustomerViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        user_id = request.user.id
        customer = models.Customer.objects.get(user_id=user_id)
        if request.method == "GET":
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = serializers.CustomerSerializer(customer)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[SendPrivateEmailToCustomerPermission])
    def send_private_email(self, request, pk):
        return Response(f"Sending to customer {pk=}")


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "options", "head"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUserOrReadOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        queryset = (
            models.Order.objects.prefetch_related(
                Prefetch(
                    "items",
                    queryset=models.OrderItem.objects.select_related("product"),
                )
            )
            .select_related("customer__user")
            .all()
        )

        if user.is_staff:
            return queryset
        return queryset.filter(customer__user_id=user.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return serializers.OrderCreateSerializer

        if self.request.method == "PATCH":
            return serializers.OrderUpdateSerializer

        if self.request.user.is_staff:
            return serializers.OrderStaffSerializer
        return serializers.OrderSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def create(self, request, *args, **kwargs):
        create_order_serializer = serializers.OrderCreateSerializer(
            data=request.data,
            context={"user_id": self.request.user.id},
        )
        create_order_serializer.is_valid(raise_exception=True)
        created_order = create_order_serializer.save()
        order_created.send_robust(self.__class__, order=created_order)
        serializer = serializers.OrderSerializer(created_order)
        return Response(serializer.data)
