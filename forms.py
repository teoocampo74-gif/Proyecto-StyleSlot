from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class RegistroForm(UserCreationForm):
    nombre = forms.CharField(
        label='Nombre completo',
        max_length=150,
        widget=forms.TextInput(attrs={'autocomplete': 'name'}),
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    telefono = forms.CharField(
        label='Teléfono',
        max_length=20,
        widget=forms.TelInput(attrs={'autocomplete': 'tel'}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['username'].widget.attrs['autocomplete'] = 'username'
        self.order_fields((
            'nombre',
            'username',
            'email',
            'telefono',
            'password1',
            'password2',
        ))

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if self._meta.model.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con este correo.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['nombre'].strip()
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
