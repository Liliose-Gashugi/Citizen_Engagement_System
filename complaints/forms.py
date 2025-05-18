from django import forms
from .models import Complaint, Agency

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['citizen_name', 'citizen_email', 'category', 'description']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate dropdown from agencies
        self.fields['category'] = forms.ChoiceField(
            choices=[(agency.name, agency.name) for agency in Agency.objects.all()],
            label="Select Category"
        )

class ResponseForm(forms.Form):
    response = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), label="Agency Response", required=True)