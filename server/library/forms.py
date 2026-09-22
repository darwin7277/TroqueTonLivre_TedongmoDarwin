from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class BootstrapMixin:
    """Ajoute les classes Bootstrap aux widgets de tous les champs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                css = 'form-check-input'
            elif isinstance(widget, forms.Select):
                css = 'form-select'
            else:
                css = 'form-control'
            existing = widget.attrs.get('class', '')
            widget.attrs['class'] = f'{existing} {css}'.strip()

User = get_user_model()

class RegisterForm(BootstrapMixin, UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username']
