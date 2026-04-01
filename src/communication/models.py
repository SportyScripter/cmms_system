from django.db import models
from django.conf import settings

class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages", verbose_name="Nadawca"
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages", verbose_name="Odbiorca"
    )
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    content = models.TextField(verbose_name="Treść wiadomości")
    
    is_read = models.BooleanField(default=False, verbose_name="Czy przeczytana?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data wysłania")
    
    def __str__(self):
        return f"Od: {self.sender} Do: {self.receiver} - {self.title}"
    
    class Meta:
        verbose_name = "Wiadomość"
        verbose_name_plural = "Wiadomości"
        ordering = ["-created_at"]