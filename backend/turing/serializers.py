from rest_framework import serializers
from .models import TuringProgram

class TuringProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TuringProgram
        fields = '__all__'