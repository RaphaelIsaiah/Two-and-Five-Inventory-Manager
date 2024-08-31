from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm


class Index(TemplateView):
    template_name = "inventory/index.html"


class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "inventory/signup.html", {"form": form})

    # Handles user sign up, authentication and login
    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
            )

            login(request, user)
            return redirect("index")

        # if the form is not valid, it renders this to avoid errors.
        return render(request, "inventory/signup.html", {"form": form})
