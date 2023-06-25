from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, MultiField, Div, Fieldset
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput(),
        help_text=_("<ul><li>Your password should contain at least 3 symbols.</li></ul>"),
    )
    password_confirm = forms.CharField(
        label=_('Password confirm'), 
        widget=forms.PasswordInput(),
        help_text=_("For confirmation please enter your password again."),
        error_messages={
                "passwords_don't match": _('Password and confirm password do not match.'),
            }
    )

    class Meta:
        model = User
        help_texts = {
            'nickname': _('Mandatory field. No more than 150 symbols. Only letters, digits and symbols @/./+/-/_.'),
        }
        error_messages = {
            'password_confirm': {
                "passwords_don't match": _('Password and confirm password do not match.'),
            }
        }
        fields = ['name', 'surname', 'nickname', 'password']
        localized_fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-userForm'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.add_input(Submit('submit', 'Register'))
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            error = _("Password and confirm password do not match.")
            raise forms.ValidationError(error)
