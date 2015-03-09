# coding=utf-8
from django.db import models
import os
from django.db.models.fields.files import ImageField, ImageFieldFile
from PIL import Image
from phonenumber_field.modelfields import PhoneNumberField

# 工具函数(1.jpg,1.jpeg->1.thumb.jpg)



def _add_thumb(s):
    """
    Modifies a string (filename, URL) containing an image filename, to insert
    '.thumb' before the file extension (which is changed to be '.jpg').CharField
    """
    parts = s.split(".")
    parts.insert(-1, "thumb")
    if parts[-1].lower() not in ("jpeg", "jpg"):
        parts[-1] = "jpg"

    return ".".join(parts)

# 缩略图
class ThumbnailImageFieldFile(ImageFieldFile):
    def _get_thumb_path(self):
        return _add_thumb(self.path)

    thumb_path = property(_get_thumb_path)

    def _get_thumb_url(self):
        return _add_thumb(self.url)

    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)
        img.thumbnail((self.field.thumb_width, self.field.thumb_height),Image.ANTIALIAS,)
        img.convert('RGB')
        file_suffix = name.split('.')[-1]
        if file_suffix.lower() == 'jpg':
            file_suffix = 'jpeg'
        img.save(self.thumb_path, file_suffix)

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)

# 缩略图类型
class ThumbnailImageField(models.ImageField):
    """
    Behaves like a regular ImageField, but stores an extra JPEG
    thumbnail image, providing get_field_thumb_url() and get_field_thumb_filename().
    Accepts two additional, optional arguments: thumb_width and thumb_height,
    both defaulting to 128 (pixels). Resizing will preserve aspect ratio while
    staying inside the requested dimensions; see PIL's Image.thumbnail()
    method documentation for details.
    """
    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)


#组别
class Team(models.Model):
    team = models.CharField(verbose_name="团队",max_length=110)

    def __unicode__(self):
        return u'%s'%(self.team)
    class Meta:
        verbose_name = "团队中心"
        verbose_name_plural = "团队"
        db_table = "Group"

# 用户
class User(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=255)
    password = models.CharField(verbose_name="密码",max_length=100)
    email = models.EmailField(blank=True,verbose_name="邮箱")
    phone = PhoneNumberField(verbose_name="联系方式",blank=True)
    team = models.ForeignKey('Team',verbose_name="团队")

    def __unicode__(self):
        return u'%s' %(self.username)

    class Meta:
        verbose_name = "用户中心"
        verbose_name_plural = "用户"
        db_table = "User"

#版本号
class Version(models.Model):
    version = models.CharField(verbose_name='版本号',max_length=20)

    def __unicode__(self):
        return u'%s'%(self.version)

    class Meta:
        verbose_name = "版本中心"
        verbose_name_plural = "版本"
        db_table = "Version"

#项目
class Project(models.Model):
    project = models.CharField(verbose_name='项目',max_length=100)
    version = models.ForeignKey(Version,verbose_name='版本')

    def __unicode__(self):
        return u'%s'%(self.project)

    class Meta:
        verbose_name = "项目中心"
        verbose_name_plural = "项目"
        db_table = "Project"


#模块
class Modules(models.Model):
    modules = models.CharField(verbose_name='模块',max_length=200)

    def __unicode__(self):
        return u'%s'%(self.modules)

    class Meta:
        verbose_name = "模块中心"
        verbose_name_plural = "模块"
        db_table = "Module"

# bug发布
class Bug(models.Model):
    urgency_Chioces = (
        ('1','低'),
        ('2','中'),
        ('3','高'),
        ('4','严重'),
    )
    platform_Chioces = (
        ('1','IOS'),
        ('2','Android'),
    )

    state_Chioces = (
        ('1','未解决'),
        ('2','正在解决'),
        ('3','已解决'),
    )

    project = models.ForeignKey(Project,verbose_name='项目')
    version = models.ForeignKey(Version,verbose_name='版本')
    distribter = models.ForeignKey(User,verbose_name='分发给',related_name='distribter')
    urgency = models.CharField(verbose_name='紧急严重',choices=urgency_Chioces,max_length=12)
    name = models.ForeignKey(User,verbose_name='发布人',related_name='name')
    content = models.TextField(max_length=500,verbose_name='问题详情')
    date = models.DateField(auto_now=True,verbose_name='时间')
    module = models.ForeignKey(Modules,verbose_name='所属模块',null=True,default = None)
    platform = models.CharField(verbose_name='平台',choices=platform_Chioces,max_length=1)
    phone = models.ForeignKey(User,verbose_name='联系方式')
    state = models.CharField(verbose_name='状态',choices=state_Chioces,max_length=1)
    pic = ThumbnailImageField(verbose_name='详情图片',upload_to='images/bug',blank=True)
    push = models.BooleanField(choices=False,verbose_name="是否推送")

    def __unicode__(self):
        return u'%s' %(self.name)

    class Meta:
        ordering = ['date']
        verbose_name = "问题中心"
        verbose_name_plural = "问题"
        db_table = "Bug"


