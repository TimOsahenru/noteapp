from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


# ......................... Like Note .....................
def like_note(request, pk):
    if request.method == 'POST':
        creator = request.user
        note_id = request.POST.get('note_id')
        note = Note.objects.get(id=note_id)

        if creator in note.likes.all():
            note.likes.remove(creator)
        else:
            note.likes.add(creator)
        like, created = Liked.objects.get_or_create(creator=creator, note_id=note_id)

        if not created:
            if like.likes == 'Like':
                like.likes == 'Unlike'
            else:
                like.likes == 'Like'
    return redirect('notes')
    # note = get_object_or_404(Note, id=request.POST.get('note_id'))
    # liked = False
    # if note.likes.filter(id=request.user.id).exits():
    #     note.likes.remove(request.user)
    #     liked = False
    #
    # note.likes.add(request.user)
    # liked = True
    # return redirect('notes')


# ....................... All notes ..................
def all_notes(request):
    notes = Note.objects.filter(publish=True)
    recent_notes = notes.order_by('-updated_date')[0:4]

    context = {'notes': notes, 'recent_notes': recent_notes}
    return render(request, 'index.html', context)
# class NoteList(ListView):
#     model = Note
#     context_object_name = 'notes'
#     template_name = '../templates/index.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(NoteList, self).get_context_data()
#         pk = self.kwargs.get('pk')
#         context['notes'] = context['notes'].filter(publish=True)
#         context['note'] = get_object_or_404(Note, id=pk)
#
#         liked = False
#         if context['note'].likes.filter(id=self.request.user.id).exists():
#             liked = True
#         context['liked'] = liked
#         return context


# ............................... Create Notes .....................
@login_required(login_url='login')
def create_note(request):
    form = NoteForm()
    page = 'create'
    creator = request.user

    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.creator = creator
            note.save()
            return redirect('profile', pk=request.user.id)
    context = {'form': form}
    return render(request, 'note-form.html', context)


# ......................... Edit notes ............................
@login_required(login_url='login')
def edit_note(request, pk):
    note = Note.objects.get(id=pk)
    form = NoteForm(instance=note)

    if request.user != note.creator:
        return redirect('profile', pk=request.user.id)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes')

    context = {'form': form}
    return render(request, 'note-form.html', context)


# ...................... Delete Note ...............................
@login_required(login_url='login')
def delete_note(request, pk):
    note = Note.objects.get(id=pk)

    if request.user != note.creator:
        return redirect('profile', pk=request.user.id)

    if request.method == 'POST':
        note.delete()
        return redirect('notes')
    context = {'note': note}
    return render(request, 'delete.html', context)


# ..................... Login View ...............................
class LoginUser(LoginView):
    page = 'login'
    template_name = '../templates/login.html'
    redirect_authenticated_user = True
    next_page = 'notes'


# .....................  SignUp View ...............................
class RegisterPage(FormView):
    form_class = CreatorCreationForm
    template_name = '../templates/signup.html'
    
    def form_valid(self, form):
        creator = form.save(commit=False)
        creator.username = creator.username.lower()
        creator = form.save()
        
        if creator is not None:
            login(self.request, creator)
            return redirect('login')
        super(RegisterPage, self).form_valid(form)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('notes')
        return super(RegisterPage, self).get(request)


# ..................... Creator's profile ................................
def creator_profile(request, pk):
    creator = Creator.objects.get(id=pk)
    notes = creator.note_set.all()
    published_notes = creator.note_set.filter(publish=True)
    unpublished_notes = creator.note_set.filter(publish=False).count()
    note_count = notes.count()

    context = {'creator': creator,
               'notes': notes,
               'note_count': note_count, 'unpublished_notes': unpublished_notes,
               'published_notes': published_notes}
    return render(request, 'creator-profile.html', context)


# ................... Creator profile update ........................
@login_required(login_url='login')
def creator_profile_update(request):
    creator = request.user
    form = CreatorUpdateForm(instance=creator)

    if request.method == 'POST':
        form = CreatorUpdateForm(request.POST, request.FILES, instance=creator)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=creator.id)
    context = {'form': form}
    return render(request, 'profile-update.html', context)


# ................... Like view ........................
# def like_note(request, pk):
#     creator = request.user
#     note = get_object_or_404(Note, id=request.POST.get('note_id'))
#     note.likes.add(creator)
#     return redirect('notes')
