from decimal import Decimal

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.catalog.models import Product
from .models import Cart, CartItem
from .serializers import (
    CartItemCreateSerializer,
    CartItemUpdateSerializer,
    CartSerializer,
)


def _recalculate_cart(cart: Cart) -> None:
    subtotal = Decimal("0.00")
    for item in cart.items.select_related("product").all():
        subtotal += Decimal(item.quantity) * item.product.price

    cart.subtotal_amount = subtotal
    cart.discount_amount = Decimal("0.00")
    cart.shipping_amount = Decimal("0.00")
    cart.total_amount = cart.subtotal_amount - cart.discount_amount + cart.shipping_amount
    cart.save(
        update_fields=[
            "subtotal_amount",
            "discount_amount",
            "shipping_amount",
            "total_amount",
            "updated_at",
        ]
    )


def _get_or_create_user_cart(user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = _get_or_create_user_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemCollectionView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = _get_or_create_user_cart(request.user)
        product = get_object_or_404(Product, id=serializer.validated_data["product_id"])
        quantity = serializer.validated_data["quantity"]

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        _recalculate_cart(cart)
        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_item(self, user, item_id: int) -> CartItem:
        cart = _get_or_create_user_cart(user)
        return get_object_or_404(CartItem.objects.select_related("cart"), id=item_id, cart=cart)

    @transaction.atomic
    def patch(self, request, item_id: int):
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = self._get_item(request.user, item_id)
        item.quantity = serializer.validated_data["quantity"]
        item.save(update_fields=["quantity"])

        _recalculate_cart(item.cart)
        return Response(CartSerializer(item.cart).data)

    @transaction.atomic
    def delete(self, request, item_id: int):
        item = self._get_item(request.user, item_id)
        cart = item.cart
        item.delete()
        _recalculate_cart(cart)
        return Response(status=status.HTTP_204_NO_CONTENT)
