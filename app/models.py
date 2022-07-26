from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.


class Customer(AbstractUser):
    is_user = models.BooleanField(default=False)

    FullName = models.CharField(max_length=25, blank=True, null=True)

    Contact_no = models.CharField(max_length=50)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)


class product(models.Model):
    ProductName = models.CharField(max_length=25)
    productBrand = models.CharField(max_length=25)
    cloth = models.CharField(max_length=25)
    size = models.FloatField()
    colour = models.CharField(max_length=25)
    TotalAmount = models.IntegerField()
    image1 = models.ImageField(upload_to='products')
    image2 = models.ImageField(upload_to='products')
    image3 = models.ImageField(upload_to='products')

    def __str__(self):
        return self.ProductName

class OrderItem(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, )
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_item_price(self):
        total = self.quantity * self.item.TotalAmount
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField(max_length=200, null=False)
    email = models.EmailField()
    phone_no = models.IntegerField()
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    pincode = models.CharField(max_length=200, null=False)


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    card_no = models.CharField(max_length=30)
    card_cvv = models.CharField(max_length=30)
    expiry_month = models.CharField(max_length=20)
    expiry_year = models.CharField(max_length=20)

class Complaint(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=50)
    complaint = models.TextField()
    date = models.DateField()
    reply = models.TextField(null=True,blank=True)






class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    completed_date = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    assigned = models.BooleanField(default=False)

    def get_total(self):
        item_total = 0
        product_total = 0

        for order_item in self.items.all():
            item_total += order_item.get_total_item_price()+10

        return item_total

class Review(models.Model):
    item = models.ForeignKey(product, on_delete=models.CASCADE, related_name='reviews', )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews', )
    rating = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
