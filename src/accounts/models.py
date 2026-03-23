from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Administrator"
        MECHANIK = "MECHANIK", "Serwisant/Mechanik"
        OPERATOR = "OPERATOR", "Operator"
        VIEWER = "VIEWER", "Przeglądjący (kierownictwo)"
        
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OPERATOR,
        verbose_name="Rola w systemie",
    )
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.get_role_display()})" if self.first_name else f"{self.username} ({self.get_role_display()})"
    
    class Meta:
        verbose_name = "Użytkownik"
        verbose_name_plural = "Użytkownicy"