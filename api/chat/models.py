import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rooms")
    name = models.CharField(max_length=255)
    online_chatters = models.ManyToManyField(to=User, blank=True)
    chatters = models.ManyToManyField(to=User, related_name="conversations")

    def get_online_count(self):
        return self.online_chatters.count()

    def join_online(self, user):
        self.online_chatters.add(user)
        self.save()

    def leave_online(self, user):
        self.online_chatters.remove(user)
        self.save()

    def join(self, user):
        self.chatters.add(user)
        self.save()

    def leave(self, user):
        self.chatters.remove(user)
        self.save()

    def __str__(self):
        return f"{self.id}"


class MessageManager(models.Manager):
    def recent_chats(self, conversation):
        return Message.objects.filter(conversation_id=conversation).order_by(
            "-timestamp"
        )[:20]

    def last_message(self, conversation):
        return Message.objects.filter(conversation_id=conversation).order_by(
            "-timestamp"
        )[0]


class Message(models.Model):
    objects = MessageManager()
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    chatter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.chatter.username}: {self.content} [{self.timestamp}]"
