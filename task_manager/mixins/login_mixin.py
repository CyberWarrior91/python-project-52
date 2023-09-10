from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _
from django.shortcuts import redirect


class UserLoginMixin(LoginRequiredMixin):
    permission_denied_message = _('You are not authorized! Please login to the system.')
    permission_denied_url = reverse_lazy('login')

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(
            self.request,
            self.get_permission_denied_message(),
            extra_tags='danger'
        )
        return redirect(self.permission_denied_url)
