from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/notes/(?P<note_id>\w+)/$', consumers.NoteConsumer.as_asgi()),
]