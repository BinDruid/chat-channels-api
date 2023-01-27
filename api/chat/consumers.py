from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .models import Conversation, Message
from .serializers import MessageSerializer


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    conversation_id = None
    conversation_name = None

    @property
    def user_belongs_to_conversation(self):
        return (
            False
            if not self.user.is_authenticated
            or (self.user.id not in self.conversation.chatters.values_list(flat=True))
            else True
        )

    def connect(self):
        print("Connected!")
        setattr(self, "user", self.scope["user"])
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        conversation = Conversation.objects.get(id=self.conversation_id)
        setattr(self, "conversation", conversation)
        setattr(self, "conversation_name", str(conversation.name))

        if not self.user_belongs_to_conversation:
            return

        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )
        self.send_json(
            {
                "type": "server_join_confirm",
                "conversation_name": conversation.name,
            }
        )
        recent_messages = Message.objects.recent_chats(self.conversation_id)
        self.send_json(
            {
                "type": "server_recent_messages",
                "messages": MessageSerializer(recent_messages, many=True).data,
            }
        )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "client_new_chat":
            message = Message.objects.create(
                conversation_id=self.conversation_id,
                chatter=self.user,
                content=content["message"],
            )
            message.save()
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "new_chat_message",
                    "message": MessageSerializer(message).data,
                },
            )
        if message_type == "client_delete_chat":
            # filtering on user field ensures that only the chatter himself
            # would delete his message not any other user
            Message.objects.get(id=content["id"], chatter=self.user).delete()
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "delete_chat_message",
                    "id": content["id"],
                },
            )
        return super().receive_json(content, **kwargs)

    def new_chat_message(self, event):
        print(event)
        self.send_json(event)

    def delete_chat_message(self, event):
        print(event)
        self.send_json(event)
