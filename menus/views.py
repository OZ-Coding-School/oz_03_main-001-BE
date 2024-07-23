from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Menu
from .serializers import MenuSerializer, MenuWithDetailSerializer


class MenuList(APIView):

    def get(self, request: Request) -> Response:
        page = int(request.GET.get("page", "1"))
        size = int(request.GET.get("size", "20"))
        category = request.GET.get("category", "bob").lower()
        offset = (page - 1) * size

        if page < 1:
            return Response("page input error", status=status.HTTP_400_BAD_REQUEST)

        if category == "":
            return Response("category input error", status=status.HTTP_400_BAD_REQUEST)

        menus = Menu.objects.filter(category=category).order_by("-id")[offset : offset + size]
        # .prefetch_related("category_set")[offset:offset + size]
        serializer = MenuSerializer(menus, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        # if not request.user.is_authenticated or request.user.status != "store":
        #     return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        serializer = MenuWithDetailSerializer(data=request.data)
        if serializer.is_valid():
            menu = serializer.save()
            return Response(MenuWithDetailSerializer(menu).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetail(APIView):
    def get(self, request: Request, pk: int) -> Response:
        try:
            menu = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        if not request.user.is_authenticated or request.user.status != "store":
            return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        menu = Menu.objects.get(pk=pk)
        menu.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
