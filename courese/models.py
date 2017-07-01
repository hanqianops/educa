"""
线学习平台将会提供课程在许多主题中。
每一个课程都将会划分为一个可配置的模块编号，
并且每个模块将会包含一个可配置的内容编号。
将会有许多类型的内容：文本，文件，图片，或者视频。
下面的例子展示了我们的课程目录的数据结构：
Subject 1
    Course 1
        Module 1
            Content 1 (images)
            Content 3 (text)
        Module 2
            Content 4 (text)
            Content 5 (file)
    Course 2
        Module 1
            Content 1 (images)
            Content 3 (text)
from django.contrib.auth.models import User
from courese.models import Subject, Course, Module
user = User.objects.latest('id')
subject = Subject.objects.latest('id')

# 第一个课程
c1 = Course.objects.create(subject=subject, owner=user, title='Course 1', slug='course1')
m1 = Module.objects.create(course=c1, title='Module 1')
m2 = Module.objects.create(course=c1, title='Module 2')
m3 = Module.objects.create(course=c1, title='Module 3', order=5)
m4 = Module.objects.create(course=c1, title='Module 4')

# 第二个课程
c2 = Course.objects.create(subject=subject, title='Course 2', slug='course2', owner=user)
m5 = Module.objects.create(course=c2, title='Module 1')
"""

from django.db import models
from  django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
class Subject(models.Model):
    """
    课程主题
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class Course(models.Model):
    """
    owner：创建这个课程的教师。
    subject：这个课程属于的主题。这是一个ForeingnKey字段指向Subject模型。
    title：课程标题。
    slug：课程的slug。之后它将会被用在URLs中。
    overview：这是一个TextFied列用来包含一个关于课程的概述。
    created：课程被创建的日期和时间。它将会被Django自动设置当创建一个新的对象，因为auto_now_add=True。
    """
    owner = models.ForeignKey(User, related_name='courses_created')
    subject = models.ForeignKey(Subject, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    students = models.ManyToManyField(User, related_name='courses_joined', blank=True)
    overview = models.TextField()
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents')
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in': ('text', 'video', 'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    """
     '%(class)s_related' = text_related,file_related,image_related

    Text：用来存储文本内容。
    File：用来存储文件，例如PDF。
    Image：用来存储图片文件。
    Video：用来存储视频。我们使用一个URLField字段来提供一个视频URL为了嵌入该视频。
    """
    owner = models.ForeignKey(User, related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()