from django.contrib import admin
from .models import InventoryItem, Category


class InventoryItemAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in InventoryItem._meta.fields]

    # The get_list_display method dynamically generates a list of all field names in the InventoryItem model. This makes it easier to manage and display all fields without manually listing them.
    search_fields = ("name", "category__name", "user__username")
    list_filter = ("category", "date_created", "user")


admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(Category)
admin.site.site_header = "INVENTORY ADMINISTRATION"
