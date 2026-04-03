import uuid
import qrcode
from io import BytesIO
from django.db import models
from django.core.files import File
from django.conf import settings


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
    supplier_name = models.CharField(
        max_length=200, blank=True, verbose_name="Preferowany dostawca (Nazwa/Kontakt)"
    )
    supplier_catalog_number = models.CharField(
        max_length=100, blank=True, verbose_name="Nr katalogowy dostawcy"
    )
    lead_time_days = models.PositiveBigIntegerField(
        null=True, blank=True, verbose_name="Czas dostawy (Lead Time w dniach)"
    )
    image = models.ImageField(
        upload_to="part_images/",
        blank=True,
        null=True,
        verbose_name="Zdjęcie poglądowe",
    )
    machines = models.ManyToManyField(
        "maintenance.Machine",
        blank=True,
        related_name="compatible_parts",
        verbose_name="Pasuje do maszyn",
    )

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = f"Part-{str(uuid.uuid4())[:8].upper()}"
        if not self.barecode_image:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(self.unique_code)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            file_name = f"{self.unique_code}.png"
            self.barecode_image.save(file_name, File(buffer), save=False)
        super().save(*args, **kwargs)

    def is_low_stock(self):
        return self.quantity <= self.min_quantity

    def __str__(self):
        return f"[{self.unique_code}] {self.name} - {self.type_model}"

    class Meta:
        verbose_name = "Część magazynowa"
        verbose_name_plural = "Części magazynowe"


class InventoryLog(models.Model):
    class TransactionType(models.TextChoices):
        ISSUE = "ISSUE", "Wydanie (Zużycie)"
        RECEIPT = "RECEIPT", "Przyjęcie (Dostawa/Zwrot)"

    part = models.ForeignKey(
        Part, on_delete=models.CASCADE, related_name="logs", verbose_name="Część"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Użytkownik",
    )
    work_order = models.ForeignKey(
        "maintenance.WorkOrder",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="used_parts",
        verbose_name="Zlecenie naprawy",
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
        default=TransactionType.ISSUE,
        verbose_name="Typ operacji",
    )
    quantity = models.PositiveIntegerField(verbose_name="Ilość")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data operacji")
    notes = models.TextField(blank=True, verbose_name="Uwagi")

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            if self.transaction_type == self.TransactionType.ISSUE:
                self.part.quantity -= self.quantity
            elif self.transaction_type == self.TransactionType.RECEIPT:
                self.part.quantity += self.quantity
            self.part.save()

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.part.name} ({self.quantity}szt.)"

    class Meta:
        verbose_name = "Log Magazynowy (Zużycie)"
        verbose_name_plural = "Logi Magazynowe"
        ordering = ["-timestamp"]
