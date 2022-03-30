from os import name
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView, View
from .models import Article, Comment, Category, Event, Person, Partner
from django.contrib import messages
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.conf import settings
import stripe 
stripe.api_key = settings.STRIPE_SECRET_KEY
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

def education(request):
    context = {
        'persons':Person.objects.all()[:3],
        'events':Event.objects.filter(is_active=True).order_by('-id')[:2],
        'articles':Article.objects.order_by('-id')[:3],
        'categories':Category.objects.order_by('-id'),
        'partners':Partner.objects.order_by('-id')
    }
    return render(request, "education.html", context)

def mentorship(request):
    context = {
        'persons':Person.objects.all()[:3],
        'events':Event.objects.filter(is_active=True).order_by('-id')[:2],
        'articles':Article.objects.order_by('-id')[:3],
        'categories':Category.objects.order_by('-id'),
        'partners':Partner.objects.order_by('-id')
    }
    return render(request, "mentorship.html", context)

def care(request):
    context = {
        'persons':Person.objects.all()[:3],
        'events':Event.objects.filter(is_active=True).order_by('-id')[:2],
        'articles':Article.objects.order_by('-id')[:3],
        'categories':Category.objects.order_by('-id'),
        'partners':Partner.objects.order_by('-id')
    }
    return render(request, "care.html", context)

def suprise(request):
    context = {
        'persons':Person.objects.all()[:3],
        'events':Event.objects.filter(is_active=True).order_by('-id')[:2],
        'articles':Article.objects.order_by('-id')[:3],
        'categories':Category.objects.order_by('-id'),
        'partners':Partner.objects.order_by('-id')
    }
    return render(request, "suprise.html", context)

def empowerment(request):
    context = {
        'persons':Person.objects.all()[:3],
        'events':Event.objects.filter(is_active=True).order_by('-id')[:2],
        'articles':Article.objects.order_by('-id')[:3],
        'categories':Category.objects.order_by('-id'),
        'partners':Partner.objects.order_by('-id')
    }
    return render(request, "empowerment.html", context)


def contact(request):
    try:
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
    except:
        messages.warning(request, "An error occured. Please try again.")
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
        'percent': min(int(event.donations / event.goal * 100), 100) if event.goal else 0,
        'categories':Category.objects.order_by('-id')
    }
    return render(request, "event_detail.html", context)

class CreatePaymentSessionView(View):
    def post(self, request, *args, **kwargs):
        try:
            event_id = self.request.POST.get("event_id", None)
            product_name = self.request.POST.get("product_name", None)
            amount = float(self.request.POST.get("amount", 0))
            if product_name is None: product_name = "Donation"
            product = stripe.Product.create(name=product_name)

            price = stripe.Price.create(
                product=product["id"],
                unit_amount=int(amount*100),
                currency='cad',
            )
            PRICE_ID = price["id"]

            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': PRICE_ID,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=YOUR_DOMAIN + f'success?product_name={event_id}&amount={amount}',
                cancel_url=YOUR_DOMAIN + 'cancel/'
            )
        except Exception as e:
            return HttpResponse(str(e))

        return redirect(checkout_session.url, code=303)

def donate(request):
    context = {
        'categories':Category.objects.order_by('-id')
    }
    return render(request, "donate.html", context)

def success(request):
    try:
        amount = request.GET.get("amount", 0)
        event_id = request.GET.get("product_name", None)
        event = get_object_or_404(Event, id=event_id)
        event.donations = event.donations + float(amount)
        event.save()
        return render(request, "success.html")
    except Exception as e:
        print(e)
        return render(request, "success.html")

def cancel(request):
    return render(request, "cancel.html")

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