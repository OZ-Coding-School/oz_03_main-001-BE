from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order
from .serializers import OrderSerializer


class OrderList(APIView):

    def get(self, request: Request) -> Response:
        page = int(request.GET.get("page", "1"))
        size = int(request.GET.get("size", "10"))
        offset = (page - 1) * size

        # TODO: USER 추가 시 filter 적용
        # user_id = request.user.id
        # total_count = Order.objects.count()

        if page < 1:
            return Response("page input error", status=status.HTTP_400_BAD_REQUEST)

        # orders = Order.objects.filter(user_id=user_id).prefetch_related("items__lunch__menus").order_by("-id")[offset : offset + size]
        orders = Order.objects.prefetch_related("items__lunch__menus").order_by("-id")[offset : offset + size]

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        # if not request.user.is_authenticated or request.user.status != "store":
        #     return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            # TODO: user 추가
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):
    def get(self, request: Request, pk: int) -> Response:
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:

        # if not request.user.is_authenticated or request.user.status != "store":
        #     return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(Order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
