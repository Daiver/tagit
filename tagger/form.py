from django import forms
from models import Person

class UploadForm(forms.Form):
    File = forms.FileField(label="File", widget=forms.FileInput(attrs={'class':'btn-success btn-large','id':'file'}),required=True)

class SelectPersonForm(forms.Form):
    PersonField = forms.ModelChoiceField(queryset=Person.objects.all(), empty_label="")

class NewPersonForm(forms.Form):
    Name = forms.CharField(label="Name", required=True)
