from django.contrib import auth
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import forms, models


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'accounts/login.html'
    authentication_form = forms.CustomLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.request.user.username
        return context

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if not user.has_valid_password:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('accounts:change_password'))
        return super().post(request, *args, **kwargs)


class CustomPasswordChangeView(PasswordChangeView):

    success_url = reverse_lazy('admin:password_change_done')

    def form_valid(self, form):
        form_kwargs = self.get_form_kwargs()
        user = form_kwargs['user']
        user_old_passwords = models.UserPassword.objects.filter(user=user)
        old_password = form_kwargs['data'].get('old_password', None)
        new_password1 = form_kwargs['data'].get('new_password1', None)
        new_password2 = form_kwargs['data'].get('new_password2', None)

        if new_password1 != new_password2:
            return self.form_invalid(form)

        dif = 0
        for char in new_password1:
            if not char in old_password:
                dif += 1
        if dif < 5:
            form.add_error(
                None, _("New password must have at least 5 diffrent characters from previous password"))
            return self.form_invalid(form)

        if new_password1 is not None and user_old_passwords.count():
            for new_pass in [
                    new_password1[1:],
                    new_password1[2:],
                    new_password1[3:],
                    new_password1[4:],
                    new_password1[:-1],
                    new_password1[:-2],
                    new_password1[:-3],
                    new_password1[:-4], ]:
                for item in user_old_passwords:
                    if check_password(new_pass, item.password):
                        form.add_error(
                            None, _("Password has already been used"))
                        return self.form_invalid(form)

        user.has_valid_password = True
        user.last_password_change = timezone.now()
        hashed_password = make_password(new_password1)
        models.UserPassword.objects.create(user=user,
                                           password=hashed_password)
        return super().form_valid(form)
