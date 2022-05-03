from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Event, Category, Tag
#from .forms import CommentForm
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .forms import *

# Create your views here.
"""
def index(request):
  posts = Post.objects.all().order_by('-pk')

  return render(
    request, 
    'index.html',
    {
      'posts': posts,
    }
  )
"""

class EventListView(LoginRequiredMixin, ListView):
  model = Event
  template_name = 'event_list.html'
  ordering = 'start_at'
  #paginate_by = 5

  def get_context_data(self, **kwargs):
    context = super(EventListView, self).get_context_data()
    context['events'] = Event.objects.all().order_by('start_at')
    for event in context['events']:
      event.form = EventForm(initial={
        'host': event.host,
        'title': event.title,
        'category': event.category,
        'tag': event.tag,
        'description': event.description,
        'head_image': event.head_image,
        'start_at': event.start_at,
        'end_at': event.end_at,
        'max_number': event.max_number,
        'is_hidden': event.is_hidden,
      })
    context['form'] = EventForm(initial={
      'max_number': 5, #일단 기본값은 5명으로
    })
    context['hosting_events'] = self.request.user.host_event_set.all().order_by('start_at')
    context['participating_events'] = self.request.user.participant_event_set.all().order_by('start_at')
    context['categories'] = Category.objects.all().order_by('name')
    context['tags'] = Tag.objects.all().order_by('name')
    return context

'''
def category_page(request, slug):
  if slug == 'no_category':
    category = '미분류'
    post_list = Post.objects.filter(category=None)
  else:  
    category = Category.objects.get(slug=slug)
    post_list = Post.objects.filter(category=category)

  return render(
    request,
    'post_list.html',
    {
      'post_list' : post_list,
      'categories' : Category.objects.all(),
      'no_category_post_count' : Post.objects.filter(category=None).count(),
      'category' : category,
    }
  )


def tag_page(request, slug):
  tag = Tag.objects.get(slug=slug)
  post_list = tag.post_set.all()

  return render(
    request,
    'post_list.html',
    {
      'post_list' : post_list,
      'tag' : tag,
      'categories' : Category.objects.all(),
      'no_category_post_count' : Post.objects.filter(category=None).count(),
    }
  )
'''