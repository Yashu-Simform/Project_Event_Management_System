from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import EmsUser
# # Register your models here.

class MyUserAdmin(UserAdmin):
        model = EmsUser
        list_display = ('username',
                        'email')
        list_filter = ('username',
                        'email')
        search_fields = ('username', )
        ordering = ('username', )
        filter_horizontal = ()
        fieldsets = UserAdmin.fieldsets + (
                (None, {'fields': ('username',)}),
        )
        # I've added this 'add_fieldset'
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'password'),
            }),
    )
        

admin.register(EmsUser, MyUserAdmin)