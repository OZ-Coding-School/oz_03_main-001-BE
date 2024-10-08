from django.db.models import Count, Prefetch, Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Menu, MenuDetailCategory
from .serializers import MenuWithDetailSerializer


class MenuList(APIView):

    def get(self, request: Request) -> Response:
        page = int(request.GET.get("page", "1"))
        size = int(request.GET.get("size", "10"))
        category = request.GET.get("category", "bob").lower()
        allergy = request.GET.get("allergy", "").lower()
        search = request.GET.get("search", "").lower()
        offset = (page - 1) * size

        allergies: list[int] = []

        if allergy == "true":
            if not request.user.is_authenticated:
                return Response({"message": "로그인 된 유저가 아닙니다"}, status=status.HTTP_403_FORBIDDEN)

            allergies = [aller.id for aller in request.user.allergies.all()]

        if page < 1:
            return Response("page input error", status=status.HTTP_400_BAD_REQUEST)

        if category == "":
            return Response("category input error", status=status.HTTP_400_BAD_REQUEST)

        menus = Menu.objects.filter(category=category)

        if allergies:
            menus = menus.annotate(
                allergy_count=Count("menu_details__allergy", filter=Q(menu_details__allergy__id__in=allergies))
            ).filter(allergy_count=0)

        if search:
            menus = menus.filter(name__icontains=search)

        total_count = menus.count()
        total_pages = (total_count - 1) // size + 1

        menu_details_prefetch = Prefetch("menu_details", queryset=MenuDetailCategory.objects.select_related("allergy"))

        menus = menus.order_by("-id").prefetch_related(menu_details_prefetch)[offset : offset + size]

        serializer = MenuWithDetailSerializer(menus, many=True)

        return Response(
            {"total_count": total_count, "total_pages": total_pages, "current_page": page, "results": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        if not request.user.is_authenticated or request.user.get_status_display() != "store":
            return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        serializer = MenuWithDetailSerializer(data=request.data, many=True)
        if serializer.is_valid():
            menu = serializer.save()
            return Response(MenuWithDetailSerializer(menu, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuDetail(APIView):
    def get(self, request: Request, pk: int) -> Response:
        try:
            menu = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuWithDetailSerializer(menu)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:

        # if not request.user.is_authenticated or request.user.status != "store":
        #     return Response({"success": False}, status=status.HTTP_403_FORBIDDEN)

        try:
            menu = Menu.objects.get(pk=pk)
        except Menu.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuWithDetailSerializer(menu, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        menu = Menu.objects.get(pk=pk)
        menu.delete()
        return Response({"success": True}, status=status.HTTP_204_NO_CONTENT)
