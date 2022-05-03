from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
#from markdownx.models import MarkdownxField
#from markdownx.utils import markdown



class Category(models.Model):
  name = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/blog/category/{self.name}'

  class Meta:
    verbose_name_plural = 'Categories'

class Tag(models.Model):
  name = models.SlugField(max_length=200, unique=True, allow_unicode=True)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return f'/blog/tag/{self.name}'


class Event(models.Model):
  host = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='host_event_set') #event를 맨처음에 올린 사람.
  title = models.CharField(max_length=200) #event 제목
  category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
  tag = models.ManyToManyField(Tag, blank=True, related_name='tag_set')

  #description = MarkdownxField()
  description = models.TextField()
  head_image = models.ImageField(upload_to='./images/%Y/%m/%d/', blank=True, null=True)

  start_at = models.DateTimeField() #event 시작 시간
  end_at = models.DateTimeField(blank=True, null=True) # '' 종료 시간(명확하지 않다면 NULL 입력)
  max_number = models.IntegerField() #인원 제한(0명은 무제한으로 처리하자)
  participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participant_event_set', blank=True) #참가자들의 foreign keys. host 제외
  #event.participants.all()로 전체 리스트 접근 가능

  created_at = models.DateTimeField(auto_now_add = True) #event 등록 시간
  updated_at = models.DateTimeField(auto_now = True) #event 업데이트 시간

  is_hidden = models.BooleanField(default=False)
  #숨기고 싶다면?
  def __str__(self):
    return f'[{self.pk}] {self.title} :: {self.host}'

  def get_absolute_url(self):
    return f'/blog/{self.pk}/'

  #def get_content_markdown(self):
  #  return markdown(self.content)
###
  def comment_set_heads(self):
    return self.comment_set.filter(comment_linked = None)

  def count_comments(self):
    return self.comment_set.all().count()
  

class Comment(models.Model): #댓글
  author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name='comment_set') #댓글 작성자
  event = models.ForeignKey('Event', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_set')
  #무슨 event에 작성하는지.
  #null로 입력되면 event에 종속되지 않는 홈화면 전체 챗에 표시될 수 있도록
  comment_linked = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True, related_name='comment_set')
  #답글 작성을 위해, 무슨 comment에 연결되었는지
  #null일 경우 일반 댓글.

  text = models.TextField() #댓글 내용

  created_at = models.DateTimeField(auto_now_add = True) #댓글 등록 시간
  updated_at = models.DateTimeField(auto_now = True) #댓글 업데이트 시간
  #time_created와 time_updated를 비교해서 댓글 '수정됨' 표시를 하자. 수동으로 업데이트하는 것보다 나을 듯.

  is_deleted = models.BooleanField(default = False)
  #상위 댓글이 삭제되면서 자동으로 답글까지 삭제되는 것을 방지.
  #아래의 clear_branch method를 이용하여, 답글이 없는 댓글을 데이터베이스에서 말끔하게 지우는게 가능하다.

  def __str__(self):
    return f'{self.author}::{self.text}'

#  def get_absolute_url(self):
#    return f'{self.post.get_absolute_url()}#comment-{self.pk}'
#
#  def get_avatar_url(self):
#    if self.author.socialaccount_set.exists():
#      return self.author.socialaccount_set.first().get_avatar_url()
#    else:
#      return 'https://doitdjango.com/avatar/id/932/b7bd38bb3a755a8f/svg/{self.author.email}'
  
  def get_head(self):
    #가장 상위 댓글을 찾는 메서드
    head = self
    while head.comment_linked:
      head = head.comment_linked
    return head
  
  def clear_branch(self):
    #comment_set(과 그 comment의 comment_set과 ...)이 전부 deleted되었을 경우, DB에 남길 의미가 없으므로 정리해주는 함수)
    def is_branch_dead(comment):
      if not comment.is_deleted:
        #해당 comment가 죽지 않았으면 당연히 branch가 살아있다
        return False
      for branch in comment.comment_set.all():
        #해당 comment가 죽었어도
        #하나의 branch라도 '완전히 죽지'않았다면 branch는 살아있다
        if not is_branch_dead(branch):
          return False
      #comment가 죽었고
      #하위 branch중에서 comment가 하나라도 살아있는 branch가 하나도 없다면 branch는 죽었다.
      return True
    
    if is_branch_dead(self):
      return self.delete()

    for comment in self.comment_set.all():
      #설령해당 branch가 죽지 않았더라도 하위 branch에 대해서 계속 검사를 실시한다.
      comment.clear_branch()