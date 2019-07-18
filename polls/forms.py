from django import forms
from django.utils import timezone
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user and not user.check_password(password):
                raise forms.ValidationError('Невірний пароль')
        else:
            raise forms.ValidationError('Користувача з таким логіном не існує')

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email',
        ]
        model = User
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'
        self.fields['password_check'].label = 'Повторіть пароль'
        self.fields['first_name'].label = 'Ім\'я'
        self.fields['last_name'].label = 'Прізвище'
        self.fields['email'].label = 'Електронна пошта'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['password_check']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Користувач з даним логіном вже існує')
        if password != password_check:
            raise forms.ValidationError('Ваші паролі не співпадають, спробуйте ще раз')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з даною електронною поштою вже існує')


class OrderForm(forms.Form):

    card = forms.CharField(max_length=16, min_length=16)
    cvv = forms.CharField(max_length=3, min_length=3)
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now(), required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['card'].label = 'Номер картки'
        self.fields['date'].label = 'Дата оформлення'
        self.fields['cvv'].label = 'CVV'