from .models import Note


class NoteRepository:
    @staticmethod
    def get_all():
        return Note.objects.all().order_by('-created_at')

    @staticmethod
    def get_by_id(note_id):
        return Note.objects.filter(id=note_id).first()

    @staticmethod
    def create(**kwargs):
        return Note.objects.create(**kwargs)

    @staticmethod
    def update(note, **kwargs):
        for key, value in kwargs.items():
            setattr(note, key, value)
        note.save()
        return note

    @staticmethod
    def delete(note):
        note.delete()

    @staticmethod
    def search(query=None, tag=None):
        notes = Note.objects.all().order_by('-created_at')

        if query:
            notes = notes.filter(title__icontains=query) | notes.filter(content__icontains=query)

        if tag:
            notes = notes.filter(tags__icontains=tag)

        return notes