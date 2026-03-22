from django.db import models

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

    def __str__(self):
        return f"{self.name} ({self.serial_number}) - {self.get_status_display()}"

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
