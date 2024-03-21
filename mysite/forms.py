# from django import forms
# from . models import Ticket

# forms.py
from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["Username", "Title", "Description", "Email", "file"]
        widgets = {
            'Email': forms.HiddenInput(),  # Hide the email field
            'Description': forms.Textarea(attrs={'class': 'form-description'}),
            'Username': forms.TextInput(attrs={'class': 'form-name'}),
            'Title': forms.TextInput(attrs={'class': 'form-title'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Email'].required = False
        self.fields['file'].required = False
