from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from task_manager.form_class import apply_placeholders


class NewUserForm(UserCreationForm):
    """
    Class to handle a form to register a user with
    certain fields that are required
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Confirm Password'),
        }

        apply_placeholders(self, placeholders)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username",
                  "password1", "password2")

    def save(self, commit=True):
        """
        Saves the form in db if valid
        :return: new user information
        """
        user = super(NewUserForm, self).save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.username = self.cleaned_data.get('username')
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserUpdateForm(NewUserForm):
    """
    Form to update user information
    """
    def clean_username(self):
        """
        Override the clean_username method to remove uniqueness validation
        """
        return self.cleaned_data.get('username')
