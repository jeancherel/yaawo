from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name',
            'email', 'phone', 'adress', 'account_type',
            'id_picture', 'id_piece', 'password',
            'password_confirmation'
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user

    def validate(self, attrs:dict):
        # validation de mot de passe
        if 'password_confirmation' not in attrs:
            raise serializers.ValidationError({'password_confirmation': 'Le mot de passe à besoin de confirmation'})

        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError({'password': 'Les mots de passe ne correspondent pas'})
        
        attrs.pop('password_confirmation', None)

        # validation de pièce d'identité
        if attrs.get("account_type") == User.AccountTypes.SELLER and attrs.get('id_piece') is None:
            raise serializers.ValidationError({'id_piece': "Vous devez fournir un document d'identité"})
        
        return super().validate(attrs)