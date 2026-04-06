from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'summary', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Not başlığını giriniz'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Not içeriğini yazınız',
                'rows': 8
            }),
            'summary': forms.Textarea(attrs={
                'placeholder': 'İsteğe bağlı kısa özet giriniz',
                'rows': 4
            }),
            'tags': forms.TextInput(attrs={
                'placeholder': 'Örn: django, yapay zekâ, proj'
            }),
        }