from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Comment, Tag, Category
from django.core.mail import EmailMessage
from django.contrib.auth.models import User

### event 참가
@login_required(login_url='login')
def joinEvent(request, event_pk):
  if request.method == 'POST':
    event = Event.objects.filter(pk=event_pk)[0]
    if not request.user in event.participant.all():
      event.participant.add(request.user)
    print(event.participant.all())
  return redirect('detail', event_pk)
### event 불참
def quitEvent(request, event_pk):
  if request.method == 'POST':
    event = Event.objects.filter(pk=event_pk)[0]
    if request.user in event.participant.all():
      event.participant.remove(request.user)
  return redirect('detail', event_pk)

### category
@login_required(login_url='login')
def createCategory(request):
  if request.method == 'POST':
    new_category = Category.objects.create(name = request.POST['name'])
  return redirect('home')
@login_required(login_url='login')
def updateCategory(request, category_pk):
  if request.method == 'POST':
    category = Category.objects.filter(pk=category_pk)[0]
    category.name = request.POST['name']
  return redirect('home')
@login_required(login_url='login')
def deleteCategory(request, category_pk):
  if request.method == 'POST':
    category = Category.objects.filter(pk=category_pk)[0]
    category.delete()
  return redirect('home')

### tag
@login_required(login_url='login')
def createTag(request):
  if request.method == 'POST':
    new_tag = Tag.objects.create(name = request.POST['name'])
  return redirect('home')
@login_required(login_url='login')
def updateTag(request, tag_pk):
  if request.method == 'POST':
    tag = Tag.objects.filter(pk=tag_pk)[0]
    tag.name = request.POST['name']
  return redirect('home')
@login_required(login_url='login')
def deleteTag(request, tag_pk):
  if request.method == 'POST':
    tag = Tag.objects.filter(pk=tag_pk)[0]
    tag.delete()
  return redirect('home')

### event
@login_required(login_url='login')
def createEvent(request):
  if request.method == 'POST':
    
    
    new_event = Event.objects.create(
      host = request.user,
      title = request.POST['title'],
      description = request.POST['description'],
      category = Category.objects.filter(pk=request.POST['category'])[0],
      #tag = request.POST['tag'],
      start_at = request.POST['start_at'],
#      end_at = request.POST['end_at'],
      max_number = request.POST['max_number']
    )
    title_post = request.POST['title']
    title = f'[멋사랑] 새로운 이벤트가 생성되었어요'
    host = request.user
    category = Category.objects.filter(pk=request.POST['category'])[0]
    description = '[본 메일은 멋사랑에서 발송된 메일입니다.]\n'
    description += '[새로운 이벤트가 생성되었어요.]\n'
    description += f'{host}님께서 작성하신 메일입니다.\n'
    description += f'제목: {title_post}\n'
    description += f'이벤트 카테고리: {category}\n'
    description += f'내용:'
    description += request.POST['description']
    description += f'\nhttp://withlion.pythonanywhere.com/detail/{new_event.pk}\n'
    description += '더 이상 이메일을 발송받기 원하지 않는다면, 멋사랑홈페이지에서 등록된 이벤트를 클릭하여 삭제해주세요\n'
    for user in User.objects.all():
      if user.email:
        email = EmailMessage(
          title,                # 제목
          description,       # 내용
          'toyoalsrl@likelion.org',     # 보내는 이메일 (settings에서 설정해서 작성안해도 됨)
          to=[user.email],  # 받는 이메일 리스트
        )
        email.send()
    if request.POST['end_at']:
      new_event.end_at = request.POST['end_at']
      new_event.save()
    return redirect('detail', new_event.pk)
  return redirect('home')

@login_required(login_url='login')
def updateEvent(request, event_pk):
  if request.method == 'POST':
    event = Event.objects.filter(pk=event_pk)[0]
    event.title = request.POST['title']
    event.description = request.POST['description']
    event.category = Category.objects.filter(pk = request.POST['category'])[0]
#    event.tag = request.POST['tag']
    event.start_at = request.POST['start_at']
    if request.POST['end_at']:
      event.end_at = request.POST['end_at']
    event.max_number = request.POST['max_number']
    event.save()
    return redirect('detail', event.pk)
  return redirect('home')

@login_required(login_url='login')
def closeEvent(request, event_pk):
  if request.method == 'POST':
    event = Event.objects.filter(pk=event_pk)[0]
    event.is_closed = True
    event.save()
  return redirect('home')

@login_required(login_url='login')
def deleteEvent(request, event_pk):
  if request.method == 'POST':
    event = Event.objects.filter(pk=event_pk)[0]
    event.delete()
  return redirect('home')

### comment
@login_required(login_url='login')
def createComment(request, event_pk, comment_pk):
  if request.method == 'POST':
    if comment_pk:
      new_comment = Comment.objects.create(author=request.user, event=Event.objects.filter(pk=event_pk)[0], comment_linked=Comment.objects.filter(pk=comment_pk)[0], text=request.POST['text'])
    else:
      new_comment = Comment.objects.create(author=request.user,
                         event=Event.objects.filter(
                           pk=event_pk)[0],
                         comment_linked=None,
                         text=request.POST['text'])     
    return redirect('detail', event_pk)              
  return redirect('home')


@login_required(login_url='login')
def updateComment(request, comment_pk):
  if request.method == 'POST':
    comment = Comment.objects.filter(pk=comment_pk)[0]
    comment.text = request.POST['text']
    comment.save()
    return redirect('detail', comment.event.pk)
  return redirect('home')


@login_required(login_url='login')
def deleteComment(request, comment_pk):
  if request.method == 'POST':
    comment = Comment.objects.filter(pk=comment_pk)[0]
    event_pk = comment.event.pk
    comment.is_deleted = True
    comment.save()
    comment.get_head().clear_branch()
    return redirect('detail', event_pk)

  return redirect('home')


# email 관리
@login_required(login_url='login')
def updateEmail(request):
  if request.method == 'POST':
    request.user.email = request.POST['email']
    request.user.save()
  return redirect('home')

@login_required(login_url='login')
def deleteEmail(request):
  request.user.email = ''
  request.user.save()
  return redirect('home')