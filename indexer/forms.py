from django import forms
from .models import VehicleAsset

class VehicleUploadForm(forms.ModelForm):
    class Meta:
        model = VehicleAsset
        fields = ['image']