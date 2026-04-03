from rest_framework import mixins, viewsets
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import Message
from .serializers import MessageSerializer

# Create your views here.


class MessageViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = MessageSerializer
    http_method_names = ["get", "post", "patch", "head", "options"]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.select_related("sender", "receiver").filter(
            Q(sender=user) | Q(receiver=user)
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        message = self.get_object()
        if message.receiver != request.user:
            raise PermissionDenied(
                "Only the receiver can update the message read status."
            )
        disallowed = set(request.data.keys()) - {"is_read"}
        if disallowed:
            raise PermissionDenied("Only the 'is_read' field can be updated.")
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)
