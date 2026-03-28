from rest_framework import serializers
from .models import Part

class PartSerializer(serializers.ModelSerializer):
    machine_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Part
        fields = ['id','name','unique_code','quantity','min_quantity','location','price','machine_list','barecode_image']
    
    def get_machine_list(self, obj):
        return [machine.name for machine in obj.machines.all()]