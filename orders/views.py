from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required


from cart.models import Cart
from .models import Order, PostCode, TextArea
from .forms import OrderCreateForm, TextAreaCraeteForm, PostCodeCreateForm
from payment.views import payment_process

# создание заказа
def order_create(request):
    
    key = None
    carts  = Cart.objects.filter(session_key = request.session.session_key)
    cart_total_amount  = carts.total_price
    if request.method == 'POST':       
        form = OrderCreateForm(request.POST)
        form_2 = TextAreaCraeteForm(request.POST)        
        if form.is_valid() and form_2.is_valid():
            # first_name = request.POST['first_name']
            # last_name = request.POST['last_name']
            # email = request.POST['email']
            # address = request.POST['address']
            # postal_code = request.POST['postal_code']
            # city = request.POST['city']
            # text = request.POST['text']
            # print( last_name, email, address, postal_code, city, text)
            order = form.save(commit=False)      
            text_area = form_2.save(commit=False)
            # проверяю существует ли order
            # if_exists = Order.objects.filter(session_key=request.session.session_key, paid=False).exists()
            order = Order.objects.filter(session_key=request.session.session_key, paid=False)
            
            if order.exists():
                # если существует обновляю его
                # order = Order.objects.filter(session_key=request.session.session_key, paid=False)
                # order.update(
                #     first_name=first_name, last_name=last_name, email=email, address=address,
                #     postal_code=postal_code, city=city)
                
                                
                     
                order.update(
                    first_name=form.cleaned_data['first_name'] , last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'], address=form.cleaned_data['address'],
                    postal_code=form.cleaned_data['postal_code'], city=form.cleaned_data['city'])

                # order_id = Order.objects.filter(session_key=request.session.session_key, paid=False)
                order_id = order.first()
                # for value in order:
                #     key = value.pk
                # print(key,'ffffffffffff')
                # text_area = TextArea.objects.filter(order = Order.objects.get(pk=key)).update(text=text)
                text_area = TextArea.objects.filter(order = order_id.pk).update(text=form_2.cleaned_data['text'])
                key = order_id.pk
                # print(key)
                return HttpResponseRedirect(
                    payment_process(order_id=key, cart_prize=cart_total_amount))
                # return HttpResponseRedirect(request,'orders/order/created.html')
            else:
                
                # если не существует создаю новый
                order.session_key = request.session.session_key        
                order.save()
                order_id = order.first()
                # order_id = Order.objects.filter(session_key=request.session.session_key, paid=False)
                # for value in order_id:
                #     key = value.pk

                key = order_id.pk
                text_area.order = Order.objects.get(id=key)
                text_area.save()
                # print('ccccc')
                return HttpResponseRedirect(
                    payment_process(order_id=key, cart_prize=cart_total_amount))
                # return HttpResponseRedirect(request,'orders/order/created.html')
    else:
        form = OrderCreateForm()
        form_2 = TextAreaCraeteForm()
        return render(request, 'orders/order/create.html', {'titl':'Оформление заказа', 'form': form, 'form_2': form_2})


# создание html-версии заказа для админа
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

# проверка статуса посылки покупателем 
def checking_orders(request):
    if request.method == 'POST': 
        form = PostCodeCreateForm(request.POST)
        
        if form.is_valid():
            post_code=PostCode.objects.filter(post_code=form.cleaned_data['order_code'])
            if post_code.exists():
                
                status = post_code.status
                return render(request, 'orders/order/answer_checking.html', {'titl':'Статус посылки', 'status': status})
            else:
              messages.warning(request, 'Такой код отсутствует. Попробуйте ввести заново')
              return render(request, 'orders/order/checking_the_tracker.html', {'titl':'Статус посылки', 'form': form})  
    else:
        form = PostCodeCreateForm()  
        return render(request, 'orders/order/checking_the_tracker.html', {'titl':'Статус посылки', 'form': form})  
