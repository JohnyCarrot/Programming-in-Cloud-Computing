from django.db import models

class Debtor(models.Model):
    CATEGORIES = [
        ("friend", "Friend"),
        ("family", "Family"),
        ("business", "Business"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=120,blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)
    start_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    is_paid = models.BooleanField(default=False,blank=True,null=True)
    category = models.CharField(max_length=16, choices=CATEGORIES,blank=True,null=True)
    note = models.TextField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return f"{self.name} - {self.amount} EUR"
