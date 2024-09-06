from django.contrib.sessions.models import Session
from cart.models import Cart


def get_user_carts(request):
    # if request.user.is_authenticated:
    #     return Cart.objects.filter(user=request.user).select_related('product')
    
    if not request.session.session_key:
        request.session.create()
    session_key = Session.objects.get(session_key=request.session.session_key)
    return Cart.objects.filter(session_key=session_key).select_related('product')