from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from event_calendar.models import User
from django.utils.translation import gettext_lazy as _


class UserCreationForm(forms.ModelForm):
    """A form for creating administrators in the admin pages."""

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ('email', 'group', 'is_superuser')

    def clean_password2(self):
        """Check that the two passwords are the same."""
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords don't match"))
        return password2

    def save(self, commit=True):  # noqa
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.save(commit=commit)
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users.

    Includes all the fields on the user, but replaces the password field with
    admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(
        help_text=_(
            "<a href=\"../password/\">Change the user's password here</a>."
        )
    )

    class Meta:
        model = User
        fields = (
            'email', 'password', 'group', 'is_superuser'
        )

    def clean_password(self):  # noqa
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    """A Custom UserAdmin class for our Admin model."""

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'group', 'is_superuser')
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password', 'group', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'group', 'password1', 'password2', 'is_superuser'
            ),
        }),
    )
    search_fields = ('email', 'group__name_sv', 'group__name_en')
    ordering = ('group', 'email',)
    filter_horizontal = ()
