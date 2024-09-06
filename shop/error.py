from django.shortcuts import render


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='shop/errors/errors_404.html', status=404)


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='shop/errors/errors_500.html', status=500)
