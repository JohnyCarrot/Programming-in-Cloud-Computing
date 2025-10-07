from django import forms
from .models import Debtor
from datetime import date
from decimal import Decimal, InvalidOperation

class DebtorForm(forms.ModelForm):
    class Meta:
        model = Debtor
        fields = [
            "name",
            "amount",
            "start_date",
            "due_date",
            "email",
            "is_paid",
            "category",
            "note",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 3:
            raise forms.ValidationError("Name must be at least 3 characters.")
        return name

    def clean_amount_due(self):
        amount = self.cleaned_data["amount"]
        try:
            dec = Decimal(amount)
        except (InvalidOperation, TypeError, ValueError):
            raise forms.ValidationError("Invalid amount.")
        if dec <= 0:
            raise forms.ValidationError("Amount must be greater than 0")
        if dec.as_tuple().exponent < -2:
            raise forms.ValidationError("Max 2 decimal places allowed")
        return amount

    def clean_due_date(self):
        d = self.cleaned_data["due_date"]
        if d < date.today():
            raise forms.ValidationError("Due cannot be in the past.")
        return d

    def clean_start_date(self):
        d = self.cleaned_data["start_date"]
        if d > date.today():
            raise forms.ValidationError("Beggining of dept cannot be in the future.")
        return d
