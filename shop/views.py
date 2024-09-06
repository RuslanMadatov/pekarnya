import json
import string

from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages


from .models import Category, Product
# from cart.forms import CartAddProductForm
from .forms import FeedbackCreateForm
from .utils import feedback_mail_admin
# from .tasks import feedback_mail_admin
# from django.views.decorators.cache import cache_page


# начальная страницы при вызове сайта
class IndexView(TemplateView):
    template_name = "shop/otcher/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titl'] = 'Пекарня у Руслана'
        return context


# страницы контактов
# class ContaktView(TemplateView):
#     template_name = 'shop/otcher/contacts.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context


# страница продуктов для каждой категории
def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    discount = request.GET.get('discount', None)
    new = request.GET.get('new', None)
    order_by = request.GET.get('order_by', None)
    
    category = get_object_or_404(Category, slug=category_slug)
    
    products = Product.objects.filter(category=category) & Product.objects.filter(available=True, quantyty__gt=1)
    # для фильтров новые товары и со скидкой
    if discount and new:
        products=products.filter(discount__gt=0.0) & products.filter(new=True)
    elif discount:
        products=products.filter(discount__gt=0.0)       
    elif new:
        products = products.filter(new=True)

    # фильтр цена по возрастанию или убыванию
    if order_by:
        products = products.order_by(order_by)    
    
    count_q = len(products)
    paginator = Paginator(products, 8)
    current_page = paginator.page(int(page))
    # buy_buttons_form = CartAddProductForm()
    titl = f"{category.name}"  
    return render(request, 'shop/product/shop_list.html',
                  {'category':category, 'products': current_page, 'title':titl, 'count':count_q})


# детальная страница товара
def product_detail(request, category_slug, slug):
    # для удаление из сессии корзины
    # session_key = request.session.session_key
    # sessionid = Session.objects.get(session_key=session_key)
    # session_data = sessionid.get_decoded()
    # print(session_data['cart'])
    # session_data['cart'] = {}
    # encoded_data = SessionStore().encode(session_data)
    # sessionid.session_data = encoded_data
    # sessionid.save()
    product = get_object_or_404(Product, slug=slug, available=True)
    # categorys = Category.objects.all()
    # cart_product_form = CartAddProductForm()
    titl = f"{product.name}"
    return render(request, 'shop/product/detail.html',
                  {'title':titl,'product': product})


# для обратной связи
def fedbackview(request):
    titl = 'Контактная форма'
    if request.method == 'POST':
        form= FeedbackCreateForm(request.POST)
        if form.is_valid():
            # антимат
            with open('antimat.json') as file:
                a = set(json.load(file))

            # subject = set(form_feedback.cleaned_data.get('subject').translate(
            #     str.maketrans('', '', string.punctuation)).lower().split())
            #  полученные даннные от формы разбиваем на слова
            name = set(form.cleaned_data.get('first_name').translate(
                str.maketrans('', '', string.punctuation)).lower().split())

            content = set(form.cleaned_data.get('content').translate(
                str.maketrans('', '', string.punctuation)).lower().split())

            all_info = name.union(content)
            # проверяем есть ли нецензурная лексика 
            if a & all_info != set():
                messages.warning(request, 'На нашем сайте запрещена нецензурная лексика')
                
                form = FeedbackCreateForm(request.POST)
                return render(request, 'shop/otcher/feedback.html',
                              {'form': form})
            else:
                form.save()
                messages.success(request, 'Спасибо Вам за сообщение! Вскоре мы на него ответим')
                feedback_mail_admin()
                return render(request, 'shop/otcher/feedback.html')

        else:
            messages.warning(request, 'Ваш отзыв не отправлен. Неправильно введен номер телефона или символы Captcha')
            form = FeedbackCreateForm(request.POST)
            return render(request, 'shop/otcher/feedback.html',
                          {'form': form, 'titl':titl})

    else:

        form= FeedbackCreateForm()
        return render(request, 'shop/otcher/feedback.html', {'form': form, 'titl':titl})
