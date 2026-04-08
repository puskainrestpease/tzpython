from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User, SessionToken, AccessRule, Product
from .auth import BearerTokenAuthentication
from .permissions import is_admin, can_do
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserProfileSerializer,
    AccessRuleSerializer,
    ProductSerializer,
)


def unauthorized():
    return Response({"detail": "неавторизован"}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    def post(self, request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        email = ser.validated_data["email"].lower()
        if User.objects.filter(email=email).exists():
            return Response({"detail": "уже существует"}, status=status.HTTP_400_BAD_REQUEST)

        user_role = None
        from .models import Role
        user_role = Role.objects.filter(slug="user").first()

        user = User(
            first_name=ser.validated_data["first_name"],
            last_name=ser.validated_data["last_name"],
            middle_name=ser.validated_data.get("middle_name", ""),
            email=email,
            role=user_role,
            is_active=True,
        )
        user.set_password(ser.validated_data["password"])
        user.save()

        return Response({"detail": "registered"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        ser = LoginSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        email = ser.validated_data["email"].lower()
        user = User.objects.filter(email=email, is_active=True).first()
        if not user or not user.check_password(ser.validated_data["password"]):
            return Response({"detail": "неверн"}, status=status.HTTP_401_UNAUTHORIZED)

        session = SessionToken.create_for_user(user)
        return Response(
            {"token": str(session.token), "expires_at": session.expires_at},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    authentication_classes = [BearerTokenAuthentication]

    def post(self, request):
        if not request.user:
            return unauthorized()

        request.auth.is_active = False
        request.auth.save(update_fields=["is_active"])
        return Response({"detail": "logged out"})


class MeView(APIView):
    authentication_classes = [BearerTokenAuthentication]

    def get(self, request):
        if not request.user:
            return unauthorized()
        return Response(UserProfileSerializer(request.user).data)

    def patch(self, request):
        if not request.user:
            return unauthorized()
        ser = UserProfileSerializer(request.user, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)

    def delete(self, request):
        if not request.user:
            return unauthorized()

        request.user.is_active = False
        request.user.save(update_fields=["is_active"])

        SessionToken.objects.filter(user=request.user, is_active=True).update(is_active=False)
        return Response({"detail": "удален"})


class RuleListView(APIView):
    authentication_classes = [BearerTokenAuthentication]

    def get(self, request):
        if not request.user:
            return unauthorized()
        if not is_admin(request.user):
            return Response({"detail": "запрещено"}, status=status.HTTP_403_FORBIDDEN)

        rules = AccessRule.objects.select_related("role", "element").all()
        data = AccessRuleSerializer(rules, many=True).data
        return Response(data)

    def post(self, request):
        if not request.user:
            return unauthorized()
        if not is_admin(request.user):
            return Response({"detail": "запрещено"}, status=status.HTTP_403_FORBIDDEN)

        ser = AccessRuleSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        rule, _created = AccessRule.objects.update_or_create(
            role_id=ser.validated_data["role"].id,
            element_id=ser.validated_data["element"].id,
            defaults={
                "read_permission": ser.validated_data.get("read_permission", False),
                "create_permission": ser.validated_data.get("create_permission", False),
                "update_permission": ser.validated_data.get("update_permission", False),
                "delete_permission": ser.validated_data.get("delete_permission", False),
            },
        )
        return Response(AccessRuleSerializer(rule).data, status=status.HTTP_200_OK)


class RuleDetailView(APIView):
    authentication_classes = [BearerTokenAuthentication]

    def patch(self, request, pk):
        if not request.user:
            return unauthorized()
        if not is_admin(request.user):
            return Response({"detail": "заперещно"}, status=status.HTTP_403_FORBIDDEN)

        rule = AccessRule.objects.filter(id=pk).first()
        if not rule:
            return Response({"detail": "не найдено"}, status=status.HTTP_404_NOT_FOUND)

        ser = AccessRuleSerializer(rule, data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data)


class ProductListView(APIView):
    authentication_classes = [BearerTokenAuthentication]

    def get(self, request):
        if not request.user:
            return unauthorized()

        if can_do(request.user, "products", "read", owner_id=request.user.id):
            if request.user.role and request.user.role.slug == "admin":
                qs = Product.objects.select_related("owner").all()
            else:
                qs = Product.objects.select_related("owner").filter(owner=request.user)
            return Response(ProductSerializer(qs, many=True).data)

        return Response({"detail": "запрещено"}, status=status.HTTP_403_FORBIDDEN)


class ProductDetailView(APIView):
    authentication_classes = [BearerTokenAuthentication]

    def get(self, request, pk):
        if not request.user:
            return unauthorized()

        product = Product.objects.select_related("owner").filter(id=pk).first()
        if not product:
            return Response({"detail": "не найдено"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.role and request.user.role.slug == "admin":
            return Response(ProductSerializer(product).data)

        if product.owner_id != request.user.id:
            return Response({"detail": "запрещено"}, status=status.HTTP_403_FORBIDDEN)

        if not can_do(request.user, "products", "read", owner_id=product.owner_id):
            return Response({"detail": "запрещено"}, status=status.HTTP_403_FORBIDDEN)

        return Response(ProductSerializer(product).data)
