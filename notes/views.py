from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Note
from .forms import NoteForm
from .repositories import NoteRepository
from .serializers import NoteSerializer
from .ai_service import generate_summary, generate_tags
from django.contrib import messages

class NoteListCreateAPIView(APIView):
    def get(self, request):
        query = request.GET.get('q')
        tag = request.GET.get('tag')

        if query or tag:
            notes = NoteRepository.search(query=query, tag=tag)
        else:
            notes = NoteRepository.get_all()

        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note = NoteRepository.create(**serializer.validated_data)
            return Response(NoteSerializer(note).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetailAPIView(APIView):
    def get(self, request, note_id):
        note = NoteRepository.get_by_id(note_id)
        if not note:
            return Response({"error": "Not bulunamadı"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, note_id):
        note = NoteRepository.get_by_id(note_id)
        if not note:
            return Response({"error": "Not bulunamadı"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            updated_note = NoteRepository.update(note, **serializer.validated_data)
            return Response(NoteSerializer(updated_note).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, note_id):
        note = NoteRepository.get_by_id(note_id)
        if not note:
            return Response({"error": "Not bulunamadı"}, status=status.HTTP_404_NOT_FOUND)

        NoteRepository.delete(note)
        return Response({"message": "Not silindi"}, status=status.HTTP_200_OK)


def home(request):
    query = request.GET.get('q', '')
    notes = Note.objects.all().order_by('-created_at')

    if query:
        notes = Note.objects.filter(title__icontains=query).order_by('-created_at') | \
                Note.objects.filter(content__icontains=query).order_by('-created_at')

    return render(request, 'notes/home.html', {'notes': notes, 'query': query})


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NoteForm()

    return render(request, 'notes/note_form.html', {'form': form})


def note_detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    return render(request, 'notes/note_detail.html', {'note': note})
from django.http import JsonResponse

def ai_generate_summary(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    summary = generate_summary(note.content)

    if summary.startswith("Özet oluşturulurken hata oluştu"):
        messages.error(request, "Özet oluşturulurken bir hata oluştu.")
    else:
        note.summary = summary
        note.save()
        messages.success(request, "Özet başarıyla oluşturuldu.")

    return redirect('note-detail', note_id=note.id)

def ai_generate_tags(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    tags = generate_tags(note.content)

    if tags.startswith("Etiket oluşturulurken hata oluştu"):
        messages.error(request, "Etiket oluşturulurken bir hata oluştu.")
    else:
        note.tags = tags.strip()
        note.save()
        messages.success(request, "Etiketler başarıyla oluşturuldu.")

    return redirect('note-detail', note_id=note.id)