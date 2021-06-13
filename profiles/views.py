from django.http import HttpResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .serializers import ProfileSerializer, ProfileCreationSerializer, PasswordUpdateSerializer
from .models import Profile
from .permissions import IsOwner, IsOwnerOrReadOnly


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request, *args, **kwargs):
        response_data = {
            'user_list': self.get_queryset()
        }
        return Response(data=response_data, template_name='user_list.html')

    def retrieve(self, request, *args, **kwargs):
        profile = self.get_object()
        response_date = {
            'profile': profile,
            'serializer': ProfileSerializer(profile),
            'password_change_form': PasswordUpdateSerializer()
        }
        return Response(data=response_date, template_name='profile.html')

    def update(self, request, *args, **kwargs):
        super(ProfileViewSet, self).update(request, *args, **kwargs)

        return HttpResponse(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super(ProfileViewSet, self).destroy(request, *args, **kwargs)

        return HttpResponse(status=status.HTTP_204_NO_CONTENT)


class ProfileCreation(CreateAPIView):
    serializer_class = ProfileCreationSerializer


class UpdatePasswordView(UpdateAPIView):
    serializer_class = PasswordUpdateSerializer
    model = Profile
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user.set_password(serializer.data.get('password1'))
            return Response(status=status.HTTP_200_OK)

        response = Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(response.__dict__)
        return response
