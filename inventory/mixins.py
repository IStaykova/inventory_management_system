from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import redirect


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    request: HttpRequest

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, 'You do not have access to this page.')
        return redirect('accounts:login')
