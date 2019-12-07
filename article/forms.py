# 引入表单类
from django import forms
# 引入文章模型
from article.models import ArticlePost
from mdeditor.fields import MDTextFormField


class ArticlePostForm(forms.ModelForm):
    '''
    表单  
        标题
        内容
    '''
    title = forms.CharField()
    body = MDTextFormField()

    class Meta:
        # 指明数据模型来源
        model = ArticlePost
        # 定义表单包含的字段
        fields = ('title', 'body')
