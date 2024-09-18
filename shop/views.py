import json
import string

from django.db.models.base import Model as Model

from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django.shortcuts import redirect, render
# from django.core.paginator import Paginator
from django.contrib import messages
from django.core.cache import cache



from .models import Category, Product
# from cart.forms import CartAddProductForm
from .forms import FeedbackCreateForm
from .utils import feedback_mail_admin
# from .tasks import feedback_mail_admin



# начальная страницы при вызове сайта
class IndexView(TemplateView):
    template_name = "shop/otcher/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titl'] = 'Пекарня у Руслана'
        return context

# страница продуктов для каждой категории
class CategoryListView(ListView):
    model = Product
    template_name = 'shop/product/shop_list.html'
    context_object_name = 'products'
    paginate_by = 8
    slug_url_kwarg = "category_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        discount = self.request.GET.get('discount', None)
        new = self.request.GET.get('new', None)
        order_by = self.request.GET.get("order_by", None)

        products_list_view = cache.get('products_list_view')
        if products_list_view is None:
          products_list_view = super().get_queryset().filter(category__slug=category_slug).filter(available=True, quantyty__gt=1)
          cache.set('product_list_view', products_list_view, 300)
        
        # для фильтров новые товары и со скидкой
        if discount and new:
          products_list_view=products_list_view.filter(discount__gt=0.0).filter(new=True)
        elif discount:
          products_list_view=products_list_view.filter(discount__gt=0.0)       
        elif new:
          products_list_view = products_list_view.filter(new=True)
        
        # фильтр цена по возрастанию или убыванию
        if order_by:
          products_list_view = products_list_view.order_by(order_by) 
        return products_list_view
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        category_list_view = cache.get('category_list_view')
       
        if category_list_view is None:
          category_list_view = Category.objects.all().get(slug=self.kwargs.get(self.slug_url_kwarg))
          cache.set('category_list_view', category_list_view, 300)
        context['category'] = category_list_view
        context['title'] = f"{category_list_view.name}"
        # context['category'] = self.set_get_cache(query=category_list_view, cache_name='category_list_view', cache_time=10 )
        # context['title'] = f"{self.set_get_cache(query=category_list_view, cache_name='category_list_view', cache_time=9 ).name}"
        return context 



class ProductDetailView(DetailView):
    template_name = 'shop/product/detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

    def get_object(self, queryset  = None) -> Model:
        product_detail_viev = cache.get('product_detail_viev')
        if product_detail_viev is None:
          product_detail_viev = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg), available=True)
          cache.set('product_detail_viev', product_detail_viev, 10)
        return product_detail_viev
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] =  self.object.name
        return context

# для обратной связи
class FeedbackView(View):
   
   def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titl'] =  'Контактная форма'
        return context
   
   def get(self, request):
        
      form = FeedbackCreateForm()
      return render(request, 'shop/otcher/feedback.html', {'form': form})
   
   def post(self, request):
      form= FeedbackCreateForm(request.POST)
      if form.is_valid():
            # антимат
            with open('antimat.json') as file:
                a = set(json.load(file))

            
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
                # feedback_mail_admin()
                return redirect('/feedback/') 
            

      else:
            messages.warning(request, 'Ваш отзыв не отправлен. Неправильно введен номер телефона или символы Captcha')
            form = FeedbackCreateForm(request.POST)
            return render(request, 'shop/otcher/feedback.html',
                          {'form': form})   
  

  
# для обратной связи
# def fedbackview(request):
#     titl = 'Контактная форма'
#     if request.method == 'POST':
#         form= FeedbackCreateForm(request.POST)
#         if form.is_valid():
#             # антимат
#             with open('antimat.json') as file:
#                 a = set(json.load(file))

#             # subject = set(form_feedback.cleaned_data.get('subject').translate(
#             #     str.maketrans('', '', string.punctuation)).lower().split())
#             #  полученные даннные от формы разбиваем на слова
#             name = set(form.cleaned_data.get('first_name').translate(
#                 str.maketrans('', '', string.punctuation)).lower().split())

#             content = set(form.cleaned_data.get('content').translate(
#                 str.maketrans('', '', string.punctuation)).lower().split())

#             all_info = name.union(content)
#             # проверяем есть ли нецензурная лексика 
#             if a & all_info != set():
#                 messages.warning(request, 'На нашем сайте запрещена нецензурная лексика')
                
#                 form = FeedbackCreateForm(request.POST)
#                 return render(request, 'shop/otcher/feedback.html',
#                               {'form': form})
#             else:
#                 form.save()
#                 messages.success(request, 'Спасибо Вам за сообщение! Вскоре мы на него ответим')
#                 feedback_mail_admin()
#                 return render(request, 'shop/otcher/feedback.html')

#         else:
#             messages.warning(request, 'Ваш отзыв не отправлен. Неправильно введен номер телефона или символы Captcha')
#             form = FeedbackCreateForm(request.POST)
#             return render(request, 'shop/otcher/feedback.html',
#                           {'form': form, 'titl':titl})

#     else:

#         form= FeedbackCreateForm()
#         return render(request, 'shop/otcher/feedback.html', {'form': form, 'titl':titl})


# страницы контактов
# class ContaktView(TemplateView):
#     template_name = 'shop/otcher/contacts.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['categories'] = Category.objects.all()
    #     return context

# страница продуктов для каждой категории
# def product_list(request, category_slug=None):
#     page = request.GET.get('page', 1)
#     discount = request.GET.get('discount', None)
#     new = request.GET.get('new', None)
#     order_by = request.GET.get('order_by', None)
    
#     category = get_object_or_404(Category, slug=category_slug)
    
#     products = Product.objects.filter(category=category) & Product.objects.filter(available=True, quantyty__gt=1)
#     # для фильтров новые товары и со скидкой
#     if discount and new:
#         products=products.filter(discount__gt=0.0) & products.filter(new=True)
#     elif discount:
#         products=products.filter(discount__gt=0.0)       
#     elif new:
#         products = products.filter(new=True)

#     # фильтр цена по возрастанию или убыванию
#     if order_by:
#         products = products.order_by(order_by)    
    
#     count_q = len(products)
#     paginator = Paginator(products, 8)
#     current_page = paginator.page(int(page))
#     # buy_buttons_form = CartAddProductForm()
#     titl = f"{category.name}"  
#     return render(request, 'shop/product/shop_list.html',
#                   {'category':category, 'products': current_page, 'title':titl, 'count':count_q})
# детальная страница товара
# def product_detail(request, category_slug, slug):
    # для удаление из сессии корзины
    # session_key = request.session.session_key
    # sessionid = Session.objects.get(session_key=session_key)
    # session_data = sessionid.get_decoded()
    # print(session_data['cart'])
    # session_data['cart'] = {}
    # encoded_data = SessionStore().encode(session_data)
    # sessionid.session_data = encoded_data
    # sessionid.save()
    # product = get_object_or_404(Product, slug=slug, available=True)
    # categorys = Category.objects.all()
    # cart_product_form = CartAddProductForm()
    # titl = f"{product.name}"
    # return render(request, 'shop/product/detail.html',
                  # {'title':titl,'product': product})
