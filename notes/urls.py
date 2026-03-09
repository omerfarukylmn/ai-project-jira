from django.urls import path
from .views import (
    NoteListCreateAPIView,
    NoteDetailAPIView,
    home,
    note_create,
    note_detail,
    ai_generate_summary,
    ai_generate_tags,
)

urlpatterns = [
    path('api/notes/', NoteListCreateAPIView.as_view(), name='note-list-create'),
    path('api/notes/<int:note_id>/', NoteDetailAPIView.as_view(), name='note-detail-api'),
    path('', home, name='home'),
    path('notes/create/', note_create, name='note-create'),
    path('notes/<int:note_id>/', note_detail, name='note-detail'),
    path('notes/<int:note_id>/ai-summary/', ai_generate_summary, name='ai-summary'),
    path('notes/<int:note_id>/ai-tags/', ai_generate_tags, name='ai-tags'),
]