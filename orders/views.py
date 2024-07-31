from rest_framework import status
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer


class OrderList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        page = int(request.GET.get("page", "1"))
        size = int(request.GET.get("size", "10"))
        offset = (page - 1) * size

        user_id = request.user.id

        if page < 1:
            return Response("page input error", status=status.HTTP_400_BAD_REQUEST)

        orders = (
            Order.objects.filter(user_id=user_id)
            .select_related("user")
            .prefetch_related("items__lunch__lunch_menu__menu")
            .order_by("-id")[offset : offset + size]
        )

        total_count = len(orders)
        total_pages = (total_count // size) + 1

        serializer = OrderSerializer(orders, many=True)
        return Response(
            {"total_count": total_count, "total_pages": total_pages, "current_page": page, "results": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk: int) -> Response:
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
