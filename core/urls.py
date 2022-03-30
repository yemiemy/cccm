from django.urls import path
from core.views import (
    home, about, contact, events, donate, 
    ArticleListView, ArticleDetailView, CategoryArticleListView, 
    comments_create_view_api, event_detail, education, mentorship, 
    suprise, care, empowerment,
    CreatePaymentSessionView,
    success,
    cancel
    )

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('contact/', contact, name="contact"),
    path('events/', events, name="events"),
    path('donate/', donate, name="donate"),
    path('events/<int:id>/<str:name>/', event_detail, name="event_detail"),
    path('service/education', education, name="education"),
    path('service/mentorship', mentorship, name="mentorship"),
    path('service/empowerment', empowerment, name="empowerment"),
    path('service/care', care, name="care"),
    path('service/suprise', suprise, name="suprise"),
    # Blog
    path('blog/', ArticleListView.as_view(), name="article_list"),
    path('article/<int:pk>/<str:slug>/', ArticleDetailView.as_view(), name="article_detail"),
    path('article/category/<str:name>/', CategoryArticleListView.as_view(), name='category'),
    path('article/comments/<int:article_id>/create/', comments_create_view_api, name='comment_create'),

    #Stripe payment
    path("create-checkout-session/", CreatePaymentSessionView.as_view(), name="create-checkout-session"),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel")
]
