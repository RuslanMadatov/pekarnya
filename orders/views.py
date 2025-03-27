from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views import View

from cart.models import Cart
from .models import Order, PostCode
from .forms import OrderCreateForm, PostCodeCreateForm
from payment.views import payment_process


# создание заказа (можно переделать в класс на основе View)
def order_create(request):
    
    # key = None
    carts  = Cart.objects.filter(session_key = request.session.session_key)
    cart_total_amount  = carts.total_price
    if request.method == 'POST':       
        form = OrderCreateForm(request.POST)       
        if form.is_valid():
            
            order = form.save(commit=False)      
            
            order = Order.objects.filter(session_key=request.session.session_key, paid=False)
            # проверяю существует ли order
            if order.exists():
                # если существует обновляю его             
                                   
                order.update(
                    first_name=form.cleaned_data['first_name'] , last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'], address=form.cleaned_data['address'],
                    postal_code=form.cleaned_data['postal_code'], city=form.cleaned_data['city'], text=form.cleaned_data['text'])

                
                order_id = order.first()
                session_key = request.session.session_key

                # key = order_id.pk
                
                return HttpResponseRedirect(
                    payment_process(session_key = request.session.session_key, cart_price=cart_total_amount))
                # return HttpResponseRedirect(request,'orders/order/created.html')
            else:
                
                # если не существует создаю новый
                order.session_key = request.session.session_key        
                order.save()
                order_id = order.first()
                
                session_key = request.session.session_key

                key = order_id.pk
                
                return HttpResponseRedirect(
                    payment_process(session_key = request.session.session_key, cart_price=cart_total_amount))
                # return HttpResponseRedirect(request,'orders/order/created.html')
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'titl':'Оформление заказа', 'form': form})


# создание html-версии заказа для админа
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

# проверка статуса посылки покупателем (нужно было разместить отдельно)
class CheckingOrdersView(View):
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titl'] =  'Статус посылки'
        return context
    
    def get(self, request):
        form = PostCodeCreateForm()
        return render(request, 'orders/order/checking_the_tracker.html', {'form': form})
    
    def post(self, request):
        form = PostCodeCreateForm(request.POST)
        if form.is_valid():
            post_code=PostCode.objects.filter(post_code=form.cleaned_data['order_code'])
            if post_code.exists():
                status = post_code.status
                return render(request, 'orders/order/answer_checking.html', {'status': status})
            else:
                messages.warning(request, 'Такой код отсутствует. Попробуйте ввести заново')
                return render(request, 'orders/order/checking_the_tracker.html', { 'form': form}) 
                
