from rest_framework import serializers
from .models import Voter, VotingPoint, User

class VotingPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingPoint
        fields = ('name',)  # asumiendo que VotingPoint tiene un campo llamado 'name'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)  # asumiendo que User tiene un campo llamado 'username'

class VoterSerializer(serializers.ModelSerializer):
    voting_point = VotingPointSerializer(read_only=True)
    coordinator = UserSerializer(read_only=True)
    created = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    modified = serializers.DateField(format="%d-%m-%Y")  # asumiendo que solo quieres la fecha

    class Meta:
        model = Voter
        fields = '__all__'