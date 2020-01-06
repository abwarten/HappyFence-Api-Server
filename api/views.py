from rest_framework import viewsets, permissions, generics, status

from .serializers import (
    CreateUserSerializer,
    UserSerializer,
    LoginUserSerializer,
    ContactSerializer,
    TodayListSerializer,
    TableListSerializer,
)
from .models import Contact, TodayList, TableList

#json response, response
from django.http import JsonResponse
from rest_framework.response import Response
#PARSER
from rest_framework.parsers import MultiPartParser, FormParser
#helper
from .helpers import modify_input_for_multiple_files
#status
from rest_framework import status
#auth
from knox.models import AuthToken

class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ContactViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class TodayListAPI(generics.GenericAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TodayListSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request):
        queryset = TodayList.objects.all()
        year = self.request.query_params.get('year', None)
        month = self.request.query_params.get('month', None)
        if month is not None and year is not None:
            date_image_filter = TodayList.objects.filter(created_at__year=year, created_at__month=month).values()
            return JsonResponse({"results": list(date_image_filter)})
        else: 
            serializer = TodayListSerializer(queryset, many=True)
            return Response(serializer.data)
        

    def post(self, request, *args, **kwargs):
        # converts querydict to original dict
        images = dict((request.data).lists())['image']
        flag = 1
        arr = []
        for image in images:
            modified_data = modify_input_for_multiple_files(image)
            file_serializer = TodayListSerializer(data=modified_data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                flag = 0

        if flag == 1:
            return Response(arr, status=status.HTTP_201_CREATED)
        else:
            return Response(arr, status=status.HTTP_400_BAD_REQUEST)

class TableViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = TableList.objects.all()
    serializer_class = TableListSerializer