from django.db import models
from django.core.validators import EmailValidator
import uuid

# Create your models here.
class Artisan(models.Model):
    # Artisans create accounts
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #uuid = models.UUIDField(auto_created=True, primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=50, validators=[EmailValidator()])
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.firstname

class Buyer(models.Model):
    # Create Buyers
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=50, validators=[EmailValidator()])
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.firstname

class Art(models.Model):
    # Store the actual art objects
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    art = models.ImageField(upload_to='images/', null=True, blank=True)
    art_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.art_name
    

class Purchase(models.Model):
    # Store objects of purchases
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    art = models.ForeignKey(Art, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=20, choices=[("paid", "Paid"), ("not paid", "Not Paid"), ("verified", "Verified")])
    dateOfpurchase = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_status

class Payment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    payment_proof = models.ImageField(upload_to='images/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Payment Proof"

class  Account(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    artisan = models.ForeignKey(Artisan, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=50)
    bank = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.account_name


