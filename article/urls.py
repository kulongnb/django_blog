# 引入path
from django.urls import path

# 正在部署的应用的名称
app_name = 'article'
from . import views

urlpatterns = [
    
    path('', views.IndexView.as_view(), name='index'),
    # path函数将url映射到视图
    path('article-list/', views.article_list, name='article_list'),
    # 文章详情
    path('article-detail/<int:id>/', views.article_detail, name='article_detail'),
    #path('article-detail2/<int:id>/',views)
    # 写文章
    path('article-create/', views.article_create, name='article_create'),
    # 删除文章
    path('article-delete/<int:id>/', views.article_delete, name='article_delete'),
    # 修改文章
    path('article-update/<int:id>/', views.article_update, name='article_update'),
]


