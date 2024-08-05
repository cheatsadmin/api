from django.contrib import admin
from cheatgame.users.models import BaseUser, Address


@admin.register(BaseUser)
class UserAdmin(admin.ModelAdmin):
    fields = ("firstname", "lastname", "phone_number", "phone_verified", "user_type")
    search_fields = ("phone_number", "lastname", "firstname")
    readonly_fields = ("phone_number", "user_type")
    list_display = (
        "firstname", "lastname", "phone_number", "phone_verified", "user_type")
    list_editable = ("phone_verified",)
    list_filter = ("user_type", "firstname", "lastname", "phone_number")


@admin.register(Address)
class UserAddressAdmin(admin.ModelAdmin):
    fields = ("province", "city", "postal_code", "address_detail", "user")
    list_display = ("province", "city", "postal_code", "address_detail", "user")
    list_filter = ("user",)
    search_fields = ("postal_code",)
