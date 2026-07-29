from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from councils.models import UserCouncils
from abc import ABC, abstractmethod


class StaffUserRequiredMixin(UserPassesTestMixin):
    permission_denied_message = "You must be a staff user to access this page."

    def get_login_url(self):
        return reverse_lazy("file_uploads:council_login_view")

    def test_func(self):
        return self.request.user.is_staff


class CouncilMatchesMixin(ABC, UserPassesTestMixin):
    permission_denied_message = "You do not have permission to access this page."

    @abstractmethod
    def get_council_id(self):
        pass

    def test_func(self):
        if self.request.user.is_staff:
            return True

        council_id = self.get_council_id()

        if (
            not self.request.user.is_active
            or not UserCouncils.objects.filter(
                user=self.request.user, council_id=council_id
            ).exists()
        ):
            return False

        return True


class ActiveUserRequiredMixin(UserPassesTestMixin):
    permission_denied_message = "You do not have permission to access this page."

    def get_login_url(self):
        return reverse_lazy("file_uploads:council_login_view")

    def test_func(self):
        return self.request.user.is_active
