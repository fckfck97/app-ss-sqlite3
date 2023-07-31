from rest_framework import serializers
from .models import Voter

class VoterSerializer(serializers.ModelSerializer):
    voting_point = serializers.StringRelatedField() # Esto usa el metod __str__ del objeto relacionado
    coordinator = serializers.StringRelatedField() 
    quarter = serializers.StringRelatedField() 
    created = serializers.DateTimeField(format="%d-%m-%Y %I:%M %p")
    modified = serializers.DateField(format="%d-%m-%Y")  # asumiendo que solo quieres la fecha

    class Meta:
        model = Voter
        fields = ['document_type', 'nuip', 'full_name', 'quarter','voting_point', 'address', 'phone', 'email', 'coordinator', 'created', 'modified']