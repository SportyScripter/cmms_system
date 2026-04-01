from rest_framework import viewsets
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer

# Create your views here.


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            Message.objects.select_related("sender", "receiver")
            .filter(Q(sender=user) | Q(receiver=user))
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
