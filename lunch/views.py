from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lunch
from .serializers import LunchSerializer


class LunchList(APIView):

    def get(self, request: Request) -> Response:
        page = int(request.GET.get("page", "1"))
        size = int(request.GET.get("size", "10"))
        offset = (page - 1) * size

        total_count = Lunch.objects.count()
        total_pages = (total_count // size) + 1

        if page < 1:
            return Response("page input error", status=status.HTTP_400_BAD_REQUEST)

        lunches = Lunch.objects.order_by("-id").prefetch_related("lunch_menu__menu")[offset : offset + size]

        serializer = LunchSerializer(lunches, many=True)
        return Response(
            {"total_count": total_count, "total_pages": total_pages, "current_page": page, "results": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        # if not request.user.is_authenticated or request.user.status != "store":
        #     return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        serializer = LunchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LunchDetail(APIView):
    def get(self, request: Request, pk: int) -> Response:
        try:
            lunch = Lunch.objects.get(pk=pk)
        except Lunch.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = LunchSerializer(lunch)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:

        # if not request.user.is_authenticated or request.user.status != "store":
        #     return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        try:
            lunch = Lunch.objects.get(pk=pk)
        except Lunch.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = LunchSerializer(lunch, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        lunch = Lunch.objects.get(pk=pk)
        lunch.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
