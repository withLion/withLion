"""WithLion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path#, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from EventApp.views import *
from EventApp.functions import *
from LoginApp.views import login, logout
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
  path('admin/', admin.site.urls),
# path('markdownx/', include('markdownx.urls')),

  path('', login_required(EventListView.as_view(), login_url='login'), name='home'),
  path('detail/<int:event_pk>/', login_required(EventListView.as_view(), login_url='login'), name='detail'),

  #event join, quit
  path('join_event/<int:event_pk>/', joinEvent, name='join_event'),
  path('quit_event/<int:event_pk>', quitEvent, name='quit_event'),

  ##cud
  path('create_category/', createCategory, name='create_category'),
  path('update_category/<int:category_pk>/', updateCategory, name='update_category'),
  path('delete_category/<int:category_pk>/', deleteCategory, name='delete_category'),
  path('create_tag/', createTag, name='create_tag'),
  path('update_tag/<int:tag_pk>/', updateTag, name='update_tag'),
  path('delete_tag/<int:tag_pk>/', deleteTag, name='delete_tag'),
  path('create_event/', createEvent, name='create_event'),
  path('update_event/<int:event_pk>/', updateEvent, name='update_event'),
  path('delete_event/<int:event_pk>/', deleteEvent, name='delete_event'),
  path('create_event/', createEvent, name='create_event'),
  path('update_event/<int:event_pk>/', updateEvent, name='update_event'),
  path('delete_event/<int:event_pk>/', deleteEvent, name='delete_event'),
  path('close_event/<int:event_pk>/', closeEvent, name='close_event'),
  path('create_comment/<int:event_pk>/<int:comment_pk>/', createComment, name='create_comment'),
  path('update_comment/<int:comment_pk>/', updateComment, name='update_comment'),
  path('delete_comment/<int:comment_pk>/', deleteComment, name='delete_comment'),

  #user email
  path('update_email/', updateEmail, name='updateEmail'),
  path('delete_email/', deleteEmail, name='deleteEmail'),
  re_path(r'^send$', MailView.as_view()),
  #login
  path('login/', login, name='login'),
  path('logout/', logout, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)