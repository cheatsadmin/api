from django.db import models
from enum import IntEnum

from cheatgame.common.models import BaseModel


class CommonQuestionLocation(IntEnum):
    ISSUE = 1

    @classmethod
    def choices(cls):
        return [(key.value , key.name) for key in cls]


class BannerLocations(IntEnum):
    FIRST = 1
    SECOND = 2
    THRID = 3
    FOURTH = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Story(models.Model):
    picture = models.FileField()
    content_picture = models.FileField()
    link = models.URLField()
    title = models.CharField(max_length=50, null=True)


class Slider(models.Model):
    laptop_picture = models.FileField()
    middle_picture = models.FileField(null=True, blank=True)
    mobile_picture = models.FileField(null=True, blank=True)
    link = models.URLField()


class Banner(models.Model):
    picture = models.FileField()
    link = models.URLField()
    location = models.IntegerField(choices=BannerLocations.choices(), unique=True)


class Blog(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=300)
    content = models.FileField()
    picture = models.FileField()


class Comment(BaseModel):
    user = models.ForeignKey("users.BaseUser", on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE, related_name="comments")
    accepted = models.BooleanField(default=False)


class BlogCategory(models.Model):
    blog = models.ForeignKey("Blog", on_delete=models.CASCADE, related_name="categories")
    category = models.ForeignKey("product.Category", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ("blog", "category")





class ContactForm(models.Model):
    subject = models.CharField(max_length=100,null=True , blank=True)
    firstname = models.CharField(max_length=100, )
    lastname = models.CharField(max_length=100, )
    phone_number = models.CharField(verbose_name="phone_number",
                                    unique=True, max_length=11)
    description = models.TextField(max_length=500, )
    is_checked = models.BooleanField(default=False)


    def __str__(self):
        return self.subject


class Message(BaseModel):
    title = models.CharField(max_length=200)
    passage= models.CharField(max_length=500)


class UserMessage(BaseModel):
    message = models.ForeignKey("Message" , on_delete=models.CASCADE , db_index=True)
    user = models.ForeignKey("users.BaseUser" ,on_delete=models.CASCADE , db_index=True)
    is_seen = models.BooleanField(default=False)


class CommonQuestion(BaseModel):
    question_location = models.IntegerField(choices=CommonQuestionLocation.choices())
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=500)
