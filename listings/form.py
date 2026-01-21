from django import forms
from django.contrib.auth.models import User
from .models import Listing,Review, Booking

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            }),
            "num_bedrooms": forms.NumberInput(attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            }),
            "num_bathrooms": forms.NumberInput(attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            }),
            "square_footage": forms.NumberInput(attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            }),
            "address": forms.TextInput(attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            }),
            "image": forms.ClearableFileInput(attrs={
                "class": "w-full text-sm text-gray-600"
            }),
        }


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
        })
    )

    class Meta:
        model = User
        fields = ["username"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500"
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password"] != cleaned_data["confirm_password"]:
            raise forms.ValidationError("Passwords do not match")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]


from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500",
                "min": date.today().strftime("%Y-%m-%d")  # минимальная дата сегодня
            }
        )
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500",
                "min": date.today().strftime("%Y-%m-%d")  # минимальная дата сегодня
            }
        )
    )
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-blue-500",
                "rows": 3,
                "placeholder": "Optional message for your booking"
            }
        )
    )

    class Meta:
        model = Booking
        fields = ["start_date", "end_date", "message"]

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and start < date.today():
            self.add_error("start_date", "Start date cannot be in the past.")
        if end and end < date.today():
            self.add_error("end_date", "End date cannot be in the past.")
        if start and end and end < start:
            self.add_error("end_date", "End date cannot be before start date.")
