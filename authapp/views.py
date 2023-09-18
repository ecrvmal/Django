from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from authapp import forms


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """
        The form_valid function is called when the form is valid.
        It's a good place to do any processing that should happen after the user has successfully submitted data.
        In this case, we're adding a message to be displayed on the next page.

        :param self: Represent the instance of the class
        :param form: Pass the form object to the view
        :return: The result of the super() call
        """
        ret = super().form_valid(form)
        message = _("Login success!<br>Hi, %(username)s") % {
            "username": self.request.user.get_full_name()
            if self.request.user.get_full_name()
            else self.request.user.get_username()
        }
        messages.add_message(self.request, messages.INFO, mark_safe(message))
        return ret

    def form_invalid(self, form):
        """
        The form_invalid function is called when the form is invalid.
        It sets a warning message on the request using Django's messaging framework.
        The message is constructed by retrieving all of the form's error messages and concatenating them into a single string.

        :param self: Access the attributes and methods of the class
        :param form: Pass the form to the template
        :return: The form with the error messages
        """
        for _unused, msg in form.error_messages.items():
            messages.add_message(
                self.request,
                messages.WARNING,
                mark_safe(f"Something goes worng:<br>{msg}"),
            )
        return self.render_to_response(self.get_context_data(form=form))


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch function is the first function called when a request is received.
        It's responsible for calling the appropriate view method based on the HTTP verb of
        the request (e.g., GET, POST, PUT, DELETE). It also handles any exceptions that may
        be raised by your view methods.

        :param self: Access the class attributes and methods
        :param request: Pass the request object to the view
        :param *args: Pass a non-keyworded, variable-length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A response object
        """
        messages.add_message(self.request, messages.INFO, _("See you later!"))
        return super().dispatch(request, *args, **kwargs)


class RegisterView(CreateView):
    model = get_user_model()
    form_class = forms.CustomUserCreationForm
    success_url = reverse_lazy("mainapp:main_page")


class ProfileEditView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = forms.CustomUserChangeForm

    def test_func(self):
        return True if self.request.user.pk == self.kwargs.get("pk") else False

    def get_success_url(self):
        return reverse_lazy("authapp:profile_edit", args=[self.request.user.pk])
