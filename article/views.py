# 引入redirect重定向模块
from django.core.paginator import Paginator
# 导入 HttpResponse 模块
from django.http import HttpResponse
from django.shortcuts import redirect, render
# 类视图
from django.views.generic import ListView

import markdown
from article.forms import ArticlePostForm

from .models import ArticlePost, User

# 引入 Q 对象
from django.db.models import Q

# 引入验证登录的装饰器
from django.contrib.auth.decorators import login_required


class IndexView(ListView):
    '''
    首页展示
    '''

    template_name = 'index.html'
    context_object_name = 'article_list'
    model = ArticlePost

    # def get_context_data(self, **kwargs):
    #     kwargs['category_list'] = ArticlePost.objects.all().order_by('name')
    #     return super(IndexView, self).get_context_data(**kwargs)


class Author(ListView):
    '''
    获取作者信息
    '''
    pass


def article_list(request):
    '''
    博客文章列表
    '''

    # 根据GET请求中查询条件
    # 返回不同排序的对象数组
    search = request.GET.get('search')
    order = request.GET.get('order')
    # 用户搜索逻辑
    if search:
        if order == 'views_counts':
            # 用 Q对象 进行联合搜索
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-views_counts')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        # 将 search 参数重置为空
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()

    # 每页显示 5 篇文章
    paginator = Paginator(article_list, 5)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # 需要传递给模板（templates）的对象
    context = {'articles': articles}

    # render函数：载入模板，并返回context对象
    return render(request, 'article/article_list.html', context)


def article_detail(request, id):
    '''
    文章详情页
    '''
    # 取出相应的文章
    article = ArticlePost.objects.get(id=id)

    # 浏览量 +1
    article.views_counts += 1
    article.save(update_fields=['views_counts'])

    # 将markdown语法渲染成html样式
    md = markdown.Markdown(
        extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
            # TOC,目录显示
            'markdown.extensions.toc',
        ])
    article.body = md.convert(article.body)

    # 需要传递给模板的对象
    context = {'article': article, 'toc': md.toc }
    # 载入模板，并返回context对象
    return render(request, 'article/article_detail.html', context)


@login_required(login_url='/userprofile/login/')
def article_create(request):
    '''
    写文章的视图
    '''
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中 id=1 的用户为作者
            # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
            # 此时请重新创建用户，并传入此用户的id
            print(new_article)
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    # 如果用户请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/article_create.html', context)


# 更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")

    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/article_update.html', context)


@login_required(login_url='/userprofile/login/')
def article_delete(request, id):
    '''
    删文章
    根据ID删除
    '''
    # 根据 id 获取需要删除的文章
    article = ArticlePost.objects.get(id=id)
    # 调用.delete()方法删除文章
    article.delete()
    # 完成删除后返回文章列表
    return redirect("article:article_list")
