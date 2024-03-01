from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib import auth
from rest_framework.views import APIView
from app_auth.serializers import UserSerializer, LoginSerializer, UserUpdateSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from app_auth.models import Account
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['fullname'] = user.fullname
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refreshToken': str(refresh),
        'accessToken': str(refresh.access_token),
    }

class UserInfoView(APIView):
    def get(self, request ):
        user = request.user
        if user.is_authenticated:
            serialized_user = UserSerializer(user).data
            return Response({'message': 'Authenticated', 'userData': serialized_user})
        else:
            return Response({'message': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegistrationView(APIView):
    # parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token = MyTokenObtainPairSerializer.get_token(user)
            serialized_user = UserSerializer(user).data
            return Response(data={'userData': serialized_user, 'refreshToken': str(token), 'accessToken': str(token.access_token)}, status=status.HTTP_201_CREATED)

        default_errors = serializer.errors
        errors = []
        for field_errors in default_errors.items():
            print(field_errors[0])
            errors.append(field_errors[1])
        return Response({'msg':errors}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            token = MyTokenObtainPairSerializer.get_token(user)
            serialized_user = UserSerializer(user).data
            return Response(data={'userData': serialized_user, 'refreshToken': str(token), 'accessToken': str(token.access_token)}, status=status.HTTP_200_OK)

        return Response({'msg':'Email or password did not matched!'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    def get_object(self, id):
        try:
            user = Account.objects.get(pk = id)
            return user
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        try:
            user = Account.objects.get(pk = id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user is not None:
            # print(data)
            serializer = UserSerializer(user)
            context = {'user':serializer.data}
            return Response(context, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, id):
        try:
            user = Account.objects.get(pk = id)
        except Account.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)            
        if user is not None:
            serializer = UserUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # user.email = request.data.get('email')
                # user.fullname = request.data.get('fullname')
                # user.save()
                return Response({"msg":"User info updated!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)