from django.contrib.auth import views as auth_views, login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView


class NewLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm


class NewLogoutView(LogoutView):
    template_name = 'logout.html'


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        new_user = authenticate(self.request, username=username, password=password)
        login(self.request, new_user)
        return super().form_valid(form)
