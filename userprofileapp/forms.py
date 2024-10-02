from django import forms
from .models import Portfolio,Experience,Education,Certification,Project
from django.forms import modelformset_factory



class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['full_name', 'bio', 'skills', 'phone_number', 'email', 'location']

        # Optional: Customize widgets for better input UI
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself...'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Comma separated skills'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
        }

    # Custom validation for the phone_number field
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_number) != 10:  # Optional: Check for exact length (e.g., 10 digits)
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone_number


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['job_title', 'company_name', 'location', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'date-field', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'class': 'date-field', 'placeholder': 'YYYY-MM-DD'}),
        }

# Education form
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school_name', 'degree', 'field_of_study', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'date-field', 'placeholder': 'YYYY-MM-DD'}),
            'end_date': forms.DateInput(attrs={'class': 'date-field', 'placeholder': 'YYYY-MM-DD'}),
        }

# Certification form
class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        fields = ['certification_name', 'issuing_organization', 'issue_date', 'expiration_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'class': 'date-field', 'placeholder': 'YYYY-MM-DD'}),
            'expiration_date': forms.DateInput(attrs={'class': 'date-field', 'placeholder': 'YYYY-MM-DD'}),
        }

# Formsets for each section
ExperienceFormset = modelformset_factory(Experience, form=ExperienceForm, extra=0)
EducationFormset = modelformset_factory(Education, form=EducationForm, extra=0)
CertificationFormset = modelformset_factory(Certification, form=CertificationForm, extra=0)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'image1', 'image2', 'github_link']
        widgets = {
            'project_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter project description'}),
            'image1': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'image2': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter GitHub link'}),
        }