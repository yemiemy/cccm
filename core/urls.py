from django.urls import path
from core.views import home, about, contact, events, donate, ArticleListView, ArticleDetailView, CategoryArticleListView, comments_create_view_api, event_detail

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('events/', events, name="events"),
    path('donate/', donate, name="donate"),
    path('events/<int:id>/<str:name>/', event_detail, name="event_detail"),

    # Blog
    path('blog/', ArticleListView.as_view(), name="article_list"),
    path('article/<int:pk>/<str:slug>/', ArticleDetailView.as_view(), name="article_detail"),
    path('article/category/<str:name>/', CategoryArticleListView.as_view(), name='category'),
    path('article/comments/<int:article_id>/create/', comments_create_view_api, name='comment_create'),
]
