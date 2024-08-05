from django.db.models import QuerySet

from cheatgame.general.filters import BlogFilter
from cheatgame.general.models import Story, Slider, Banner, Blog, Message, UserMessage, CommonQuestion, Comment
from cheatgame.users.models import BaseUser


def get_stories() -> QuerySet[Story]:
    return Story.objects.all()


def get_sliders() -> QuerySet[Slider]:
    return Slider.objects.all()


def get_banners() -> QuerySet[Banner]:
    return Banner.objects.all()


def blog_list(*, filters=None) -> QuerySet[Blog]:
    filters = filters or {}
    qs = Blog.objects.all()
    return BlogFilter(filters, qs).qs


def get_blog(slug: str) -> Blog:
    return Blog.objects.prefetch_related('categories').get(slug=slug)

def get_message_list() -> QuerySet[Message]:
    return Message.objects.all()

def get_user_message_list(* , user:BaseUser) ->QuerySet[UserMessage]:
    return UserMessage.objects.filter(user = user)

def get_common_question_list() -> QuerySet[CommonQuestion]:
    return CommonQuestion.objects.all()


def get_comment_list_blog(* , blog:Blog) -> QuerySet[Comment]:
    return Comment.objects.filter(blog=blog)




