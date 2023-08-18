from django.forms import ModelForm
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelCreateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': _('Name'),
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')
    
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Name'),
        }
