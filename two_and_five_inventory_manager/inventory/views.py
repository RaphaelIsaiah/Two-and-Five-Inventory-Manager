from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from two_and_five_inventory_manager.settings import LOW_QUANTITY
from django.contrib import messages


class Index(TemplateView):
    template_name = "inventory/index.html"


class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=self.request.user.id).order_by(
            "id"
        )  # gets all the items for this user and orders them by the id.

        low_inventory = InventoryItem.objects.filter(
            user=self.request.user.id, quantity__lte=LOW_QUANTITY
        )
        # Removing the "user=self.request.user.id" will make all entries made by any user available to all users, but since we want entries unique to each user we leave it there.

        # Error Messages that show when inventory count is low
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(
                    request, f"{low_inventory.count()} items have low inventory"
                )
            else:
                messages.error(
                    request, f"{low_inventory.count()} item has low inventory"
                )

        low_inventory_ids = InventoryItem.objects.filter(
            user=self.request.user.id, quantity__lte=LOW_QUANTITY
        ).values_list("id", flat=True)

        return render(
            request,
            "inventory/dashboard.html",
            {"items": items, "low_inventory_ids": low_inventory_ids},
        )


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


class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = (
        "inventory/item_form.html"  # html template that renders to the screen
    )
    success_url = reverse_lazy("dashboard")  # redirects to the dashboard page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # gets the original context
        context["categories"] = Category.objects.all()  # adds a value to it
        return context  # returns the context dictionary after the change

    # removes the risk of errror
    # sets the user on the form by default to be the loggedin user
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = "inventory/item_form.html"
    success_url = reverse_lazy("dashboard")


class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = "inventory/delete_item.html"
    success_url = reverse_lazy("dashboard")
    context_object_name = "item"
