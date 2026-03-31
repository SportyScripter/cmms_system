from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File

# Create your models here.


class Machine(models.Model):
    class Status(models.TextChoices):
        OPERATIONAL = "OP", "Sprawna"
        MAINTENANCE = "MA", "W trakcie przeglądu"
        BROKEN = "BR", "Awaria"

    name = models.CharField(max_length=200, verbose_name="Nazwa maszyny")
    serial_number = models.CharField(
        max_length=100, unique=True, verbose_name="Numer seryjny/Inwentarzowy"
    )
    location = models.CharField(
        max_length=100, db_index=True, verbose_name="Lokalizacja (Hala/Linia)"
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.OPERATIONAL,
        verbose_name="Status",
    )
    manufacturer = models.CharField(
        max_length=100, blank=True, verbose_name="Producent"
    )
    year_of_production = models.IntegerField(
        null=True, blank=True, verbose_name="Rok produkcji"
    )
    documentation = models.FileField(
        upload_to="machine_docs/",
        blank=True,
        null=True,
        verbose_name="Dokumentacja (PDF)",
    )
    qr_code_image = models.ImageField(
        upload_to="machine_qrs/", blank=True, null=True, verbose_name="Kod QR Maszyny"
    )

    def __str__(self):
        return f"{self.name} ({self.serial_number}) - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        generate_qr = False

        # Determine if this is an update and whether the serial number has changed.
        old_serial_number = None
        if self.pk:
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
                old_serial_number = old_instance.serial_number
            except self.__class__.DoesNotExist:
                old_serial_number = None

        # Generate QR if it does not exist yet or if the serial number has changed.
        if self.serial_number:
            if not self.qr_code_image:
                generate_qr = True
            elif (
                old_serial_number is not None
                and old_serial_number != self.serial_number
            ):
                generate_qr = True

        if generate_qr:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(f"MACHINE-{self.serial_number}")
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            file_name = f"qr_machine_{self.serial_number}.png"
            self.qr_code_image.save(file_name, File(buffer), save=False)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Maszyna"
        verbose_name_plural = "Maszyny"


class WorkOrder(models.Model):
    class Priority(models.TextChoices):
        LOW = "L", "Niski"
        MEDIUM = "M", "Średni"
        HIGH = "H", "Wysoki"
        CRITICAL = "C", "Krytyczny"

    class Status(models.TextChoices):
        PENDING = "P", "Oczekujące"
        IN_PROGRESS = "I", "W trakcie"
        COMPLETED = "C", "Zakończone"

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="work_orders",
        verbose_name="Maszyna",
    )
    title = models.CharField(max_length=200, verbose_name="Tytuł zgłoszenia")
    description = models.TextField(
        blank=True, verbose_name="Opis problemu / Zakres prac"
    )
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        verbose_name="Priorytet",
    )
    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Status",
    )
    photo = models.ImageField(
        upload_to="work_order_photos/",
        blank=True,
        null=True,
        verbose_name="Zdjęcie usterki",
    )
    completed_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Data i czas zakończenia naprawy"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Data ostatniej aktualizacji"
    )

    def __str__(self):
        return f"Zlecenie #{self.id} - {self.title}"

    class Meta:
        verbose_name = "Zlecenie naprawy"
        verbose_name_plural = "Zlecenia naprawy"
        ordering = ["-created_at"]


class MaintenanceSchedule(models.Model):
    title = models.CharField(max_length=200, verbose_name="Nazwa przeglądy/zadania")
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="schedules",
        verbose_name="Maszyna",
    )
    description = models.TextField(blank=True, verbose_name="Zakres prac")
    interval_days = models.PositiveIntegerField(
        verbose_name="Częstotliwość (dni)",
        help_text="Co ile dni należy powtarzać zadanie? (0 jeśli jednorozowe)",
    )
    next_due_date = models.DateField(
        verbose_name="Data najbliższego wykonania", null=True, blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Czy aktywne?")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.machine.name} (Termin: {self.next_due_date})"

    class Meta:
        verbose_name = "Harmonogram przeglądu"
        verbose_name_plural = "Harmonogramy przeglądów"
        ordering = ["next_due_date"]
