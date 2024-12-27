from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from .models import User

class UserViewSet(ModelViewSet):

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
    
    @action(methods=['post'], detail=False, url_name='login')
    def login(self, request):
        user = authenticate(
            request,
            username=request.data['username'],
            password=request.data['password']
        )

        if user is not None:
            token = Token.objects.get_or_create(user=user)
            return Response({
                'token': token[0].key,
                'user': UserSerializer(user).data
            }, 200)
        
        return Response({'error': "Identifiant ou mot de passe incorrect !"}, 400)
    
    @action(methods=['post'], detail=False, url_name='logout')
    def logout(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': 'Déconnexion réussie'}, 200)
        except Token.DoesNotExist:
            return Response({'error': "Vous n'êtes pas connecté"}, 400)