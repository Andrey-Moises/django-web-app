from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Article, UserProfile

class ArticleAdmin(admin.ModelAdmin):
    list_display    = ("title", "word_count", "status", "created_at", "updated_at")
    list_filter     = ("status",)
    search_fields   = ("title", "content")
    date_hierarchy  = "created_at"
    ordering        = ("created_at",)
    readonly_fields = ("word_count", "created_at", "updated_at")

class CustomUserAdmin(UserAdmin):
    fieldsets = ( # A fieldset is a group of fields displayed together in the admin form.
        (None             , {"fields": ("email", "password")}),
        ("Personal info"  , {"fields": ("first_name", "last_name")}),
        ("Permissions"    , {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = ( # The add_fieldsets attribute is used to define the fields that will be displayed in the admin form when creating a new user.
        (None, {
            "classes": ("wide",),
            "fields" : ("email", "password1", "password2")
        }),
    )
    list_display  = ("email", "is_staff", "is_active") # The list_display attribute is used to define the fields that will be displayed in the admin list view.
    list_filter   = ("is_staff", "is_active") # The list_filter attribute is used to define the fields that will be displayed in the admin filter sidebar.
    search_fields = ("email",) # The search_fields attribute is used to define the fields that will be displayed in the admin search bar.
    ordering      = ("email",) # The ordering attribute is used to define the fields that will be displayed in the admin list view in the order specified.


# Register your models here.
admin.site.register(Article, ArticleAdmin)
admin.site.register(UserProfile, CustomUserAdmin)

