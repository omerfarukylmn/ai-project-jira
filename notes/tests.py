from django.test import TestCase
from unittest.mock import patch

from .models import Note
from .ai_service import generate_summary, generate_tags


class NoteModelTest(TestCase):
    def test_note_creation(self):
        note = Note.objects.create(
            title="Test Notu",
            content="Bu bir test notudur.",
            summary="Kısa özet",
            tags="test, django"
        )

        self.assertEqual(note.title, "Test Notu")
        self.assertEqual(note.content, "Bu bir test notudur.")
        self.assertEqual(note.summary, "Kısa özet")
        self.assertEqual(note.tags, "test, django")


class AIServiceTest(TestCase):
    @patch("notes.ai_service._call_ollama")
    def test_generate_summary(self, mock_ollama):
        mock_ollama.return_value = "Bu metnin kısa özetidir."

        result = generate_summary("Uzun bir test metni.")

        self.assertEqual(result, "Bu metnin kısa özetidir.")

    @patch("notes.ai_service._call_ollama")
    def test_generate_tags(self, mock_ollama):
        mock_ollama.return_value = "django, yapay zeka, not, özet"

        result = generate_tags("Django ile AI destekli not uygulaması.")

        self.assertEqual(result, "django, yapay zeka, not, özet")
