from django.db import models
# 导入内建的AbstractUser模型。
from django.contrib.auth.models import AbstractUser
# timezone 用于处理时间相关事务。
from django.utils import timezone


class User(AbstractUser):
    '''
    用户定义
    '''
    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        verbose_name_plural = '用户'


class ArticlePost(models.Model):
    '''
    博客文章数据模型
    '''
    # 文章作者。参数 on_delete 用于指定数据删除的方式
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()
    # 文章浏览量  PositiveIntegerField是用于存储正整数的字段
    views_counts = models.PositiveIntegerField(default=0)
    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)

    # 内部类 class Meta 用于给 model 定义元数据

    class Meta:
        # ordering 指定模型返回的数据的排列顺序
        # '-created' 表明数据应该以倒序排列
        ordering = ('-views_counts',)
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
        # return self.title 将文章标题返回
        return self.title
