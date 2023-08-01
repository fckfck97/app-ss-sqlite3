from rest_framework import serializers
from .models import Voter, OfficialConsultation, VotingPoint

class ConsultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficialConsultation
        fields = '__all__'

class VotingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VotingPoint
        fields = ['name','longitude','latitude']

class VoterSerializer(serializers.ModelSerializer):
    voting_point = VotingSerializer()
    coordinator = serializers.StringRelatedField() 
    quarter = serializers.StringRelatedField() 
    created_add = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    update_add = serializers.DateField(format="%d-%m-%Y %I:%M %p")  # asumiendo que solo quieres la fecha
    official_consultation = ConsultSerializer()
    
    class Meta:
        model = Voter
        fields = ['id','document_type', 'nuip', 'full_name', 'quarter','voting_point', 'address', 'phone', 'email', 'coordinator', 'created_add', 'update_add','official_consultation','checkout']