from django import forms
from django.forms import inlineformset_factory
from .models import Course, Module, Lesson
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Profile

User = get_user_model()

class CourseUploadForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'master_category', 'title', 'thumbnail',
            'description', 'price', 'discount_price',
            'level', 'is_live', 'is_active'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter course title'}),
            'master_category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'is_live': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Module Title'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:80px;'}),
        }

ModuleFormSet = inlineformset_factory(
    Course, Module, form=ModuleForm,
    extra=1, can_delete=True
)

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-light border-0'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control bg-light border-0'}))
    
    user_type = forms.ChoiceField(
        choices=[('Student', 'Student'), ('Teacher', 'Teacher')],
        widget=forms.Select(attrs={'class': 'form-select bg-light border-0'})
    )

    # --- NEW TEACHER SPECIFIC FIELDS ---
    qualification = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-light border-0', 
            'placeholder': 'Highest Qualification (e.g. M.Sc, PhD)'
        })
    )
    experience_years = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control bg-light border-0', 
            'placeholder': 'Total Experience in Years'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control bg-light border-0', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        user_type = cleaned_data.get("user_type")

        # Basic Password Validation
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        # Logical Validation: Ensure Teachers provide their background
        if user_type == 'Teacher':
            if not cleaned_data.get("qualification"):
                self.add_error('qualification', "Teachers must provide their qualification.")
            if cleaned_data.get("experience_years") is None:
                self.add_error('experience_years', "Teachers must provide years of experience.")

        return cleaned_data
    
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True) # Email compulsory karo

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    # ✅ Email Unique Check (Optional but Recommended)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check karo: Kya ye email kisi AUR user ke paas hai? 
        # (Self ko exclude karke check kar rahe hain)
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already registered with another account.")
        return email

class ProfileUpdateForm(forms.ModelForm):
    # Phone number validation
    phone_number = forms.CharField(
        required=True,
        min_length=10,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter 10 digit number',
            'oninput': "this.value = this.value.replace(/[^0-9]/g, '');"
        }),
        error_messages={
            'required': 'Mobile number is required.',
            'min_length': 'Mobile number must be exactly 10 digits.',
        }
    )

    class Meta:
        model = Profile
        fields = ['photo', 'phone_number', 'enrollment_number', 'branch', 
                  'college_name', 'qualification', 'experience_years','date_of_birth', 'bio']
        
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'enrollment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'branch': forms.TextInput(attrs={'class': 'form-control'}),
            'college_name': forms.TextInput(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            # ✅ 2. Experience ke liye widget bhi add kar do taaki styling sahi rahe
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Years of Experience'
            }),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

        # Sabhi fields ke liye professional English error messages
        error_messages = {
            'enrollment_number': {'required': 'Enrollment number cannot be empty.'},
            'branch': {'required': 'Please enter your branch/stream.'},
            'college_name': {'required': 'College name is required.'},
            'qualification': {'required': 'Current qualification is required.'},
            'date_of_birth': {'required': 'Date of birth is mandatory.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check karo ki user Student hai ya Teacher
        user_type = self.instance.user_type if self.instance else None
        
        for field in self.fields:
            if field == 'bio' or field == 'photo':
                self.fields[field].required = False
            # Agar user Student NAHI hai, toh academic fields optional kar do
            elif user_type != 'Student' and field in ['enrollment_number', 'branch', 'college_name', 'qualification', 'date_of_birth']:
                self.fields[field].required = False
            else:
                self.fields[field].required = True


class ReplyForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 5, 
            'placeholder': 'Write your reply to the student...'
        })
    )