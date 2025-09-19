from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from django import forms

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

class NewConversationForm(forms.Form):
    participants = forms.ModelMultipleChoiceField(queryset=User.objects.all())

@login_required
def conversation_list(request):
    conversations = request.user.conversations.all().order_by('-created_at')
    return render(request, 'Messages/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = MessageForm()
    return render(request, 'Messages/conversation_detail.html', {'conversation': conversation, 'messages': messages, 'form': form})

@login_required
def new_conversation(request):
    if request.method == 'POST':
        form = NewConversationForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create()
            conversation.participants.set(form.cleaned_data['participants'] | User.objects.filter(id=request.user.id))
            conversation.save()
            return redirect('conversation_detail', conversation_id=conversation.id)
    else:
        form = NewConversationForm()
    return render(request, 'Messages/new_conversation.html', {'form': form})
