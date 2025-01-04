from django import forms
from .models import*

class Projectform(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class Taskform(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class Profileform(forms.ModelForm):
    class Meta:
        model = Profile
        exclude=['us']

class Commentform(forms.ModelForm):
    class Meta:
        model = Comment
        fields=['comment']
       
class Statusform(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['status']