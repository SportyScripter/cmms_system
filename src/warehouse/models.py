from django.db import models
import uuid


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nazwa kategorii")
    description = models.TextField(blank=True, verbose_name="Opis")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"


class Part(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="parts",
        verbose_name="Kategoria",
    )
    name = models.CharField(max_length=200, verbose_name="Nazwa części")
    type_model = models.CharField(max_length=100, blank=True, verbose_name="Typ/Model")
    # --- Identyfikacja ---
    unique_code = models.CharField(
        max_length=50, unique=True, blank=True, verbose_name="Unikalny kod (SKU)"
    )
    barecode_image = models.ImageField(
        upload_to="barcodes/", blank=True, null=True, verbose_name="Kod kreskowy/QR"
    )

    # --- Stan i Lokalizacja ---
    quantity = models.IntegerField(default=0, verbose_name="Ilość na stanie")
    min_quantity = models.IntegerField(default=1, verbose_name="Stan minimalny (Alert)")
    location = models.CharField(
        max_length=500, blank=True, verbose_name="Lokalizacja (Regał/Półka)"
    )

    # --- Informacje Dodatkowe ---
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Cena netto (PLN)",
    )
    supplier_link = models.URLField(
        max_length=500, blank=True, verbose_name="Link do dostawcy/dokumentacji"
    )
    image = models.ImageField(
        upload_to="part_images/",
        blank=True,
        null=True,
        verbose_name="Zdjęcie poglądowe",
    )
    assigment = models.CharField(
        max_length=500, blank=True, verbose_name="Przeznaczenie/Opis"
    )

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = f"Part-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

    def is_low_stock(self):
        return self.quantity <= self.min_quantity

    def __str__(self):
        return (
            f"[{self.unique_code}] {self.name} - {self.type_model} - {self.assigment}"
        )

    class Meta:
        verbose_name = "Część magazynowa"
        verbose_name_plural = "Części magazynowe"
