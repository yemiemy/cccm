from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from .models import Article, Comment, Category, Event, Person, Partner
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
import stripe 
stripe.api_key = 'sk_test_26PHem9AhJZvU623DfE1x4sd'
# Create your views here.

YOUR_DOMAIN = "http://127.0.0.1:8000/"

def home(request):
    context = {
        'persons':Person.objects.all()[:3],
        'events':Event.objects.filter(is_active=True).order_by('-id')[:2],
        'articles':Article.objects.order_by('-id')[:3],
        'categories':Category.objects.order_by('-id'),
        'partners':Partner.objects.order_by('-id')
    }
    return render(request, "index.html", context)

def about(request):
    context = {
        'persons':Person.objects.all(),
        'categories':Category.objects.order_by('-id'),
        'partners':Partner.objects.order_by('-id')
    }
    return render(request, "about.html", context)

def contact(request):
    # try:
    if request.method == "POST":
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        subject = request.POST.get("subject", None)
        message = request.POST.get("message", None)

        context = {
            'name':name,
            'subject':subject,
            'email':email,
            'message':message
        }
        
        msg_content_admin = render_to_string('emails/contact_form_admin.txt', context)
        msg_content_user = render_to_string('emails/contact_form_user.txt', context)
        message_to_admin = (subject, msg_content_admin, 'info@communitycenterchildrenmission.ca', ['info@communitycenterchildrenmission.ca'])
        message_to_user = (subject, msg_content_user, 'info@communitycenterchildrenmission.ca', [email])  

        send_mass_mail((message_to_user, message_to_admin), fail_silently=False)
        messages.success(request, "Your message has been successfully sent.")
    return render(request, "contact.html", {'categories':Category.objects.order_by('-id')})

def events(request):
    context = {
        'events':Event.objects.filter(is_active=True).order_by('-id'),
        'categories':Category.objects.order_by('-id')
    }
    return render(request, "event.html", context)

def event_detail(request, id, name):
    event = get_object_or_404(Event, id=id)

    context = {
        'event':event,
        'percent': min(int(event.donations / event.goal * 100), 100),
        'categories':Category.objects.order_by('-id')
    }
    return render(request, "event_detail.html", context)

class CreatePaymentSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price': '{{PRICE_ID}}',
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + '/success/',
                cancel_url=YOUR_DOMAIN + '/cancel/',
            )
        except Exception as e:
            return str(e)

def donate(request):
    context = {
        'categories':Category.objects.order_by('-id')
    }
    return render(request, "donate.html", context)


# Articles Views
class ArticleListView(ListView):
    model = Article
    template_name = 'Article/article_list.html'
    ordering = ['-id']
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all().order_by('-id')
        }) 
        print(context) 
        return context

class ArticleDetailView(DetailView):
    model=Article
    template_name = 'Article/article_detail.html'
    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['related_articles'] = set(Article.objects.filter(category=self.get_object().category, is_active=True).exclude(id=self.kwargs.get('pk'))[:3])
        context['categories'] = Category.objects.order_by('-id')
        return context

class CategoryArticleListView(ListView):
    model = Article
    template_name = 'Article/article_list.html'
    paginate_by = 4
    ordering = ['-id']

    def get_queryset(self):
        category = get_object_or_404(Category, name__iexact=self.kwargs.get('name'))
        return Article.objects.filter(category=category, is_active=True).order_by('-id')
    
    def get_context_data(self, *args, **kwargs):
        context = super(CategoryArticleListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.order_by('-id')
        return context

def comments_create_view_api(request, article_id):
    if request.method == "POST":
        name = request.POST.get("name", None)
        content = request.POST.get("content", None)
        
    article = Article.objects.get(id=article_id)

    Comment.objects.create(
        article=article,
        name=name,
        content=content
    )
    return reverse('article_detail', kwargs={"pk":article_id, "slug":article.slug})