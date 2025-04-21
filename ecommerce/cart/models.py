from django.db import models


class Order(models.Model):
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)    
    client_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Pedido {self.code}"