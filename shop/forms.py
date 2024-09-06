
from django import forms
from simplemathcaptcha.fields import MathCaptchaField
from simplemathcaptcha.widgets import MathCaptchaWidget
# from captcha.fields import CaptchaField
from phonenumber_field.formfields import PhoneNumberField
from .models import Feedback


class FeedbackCreateForm(forms.ModelForm):
    
    """
    Форма отправки обратной связи
    """

    class Meta:
        model = Feedback
        fields = ('subject', 'first_name', 'phone_number', 'email', 'content')
        # widgets = {'first_name': forms.TextInput(attrs={'placeholder': 'Иван', 'aria-label': 'Иван'}),
        #            'phone_number': forms.TextInput(attrs={'placeholder': '89166291895', 'aria-label': '89166291895'})}
        
    
    captcha = MathCaptchaField(widget=MathCaptchaWidget(question_tmpl='Сколько будет %(num1)i %(operator)s %(num2)i? '))
    subject = forms.ChoiceField(choices=(("Отзыв", "Отзыв"), ("Претензия", "Претензия")))

    # subject = forms.CharField()
    first_name = forms.CharField()
    phone_number = PhoneNumberField()
    email = forms.CharField()
    content = forms.CharField()



    # def __init__(self, *args, **kwargs):
    #     """
    #     Обновление стилей формы
    #     """
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})
