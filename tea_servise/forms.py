from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
	"""Авторизация - перебрасывает пользователя в его пространство"""
	password = forms.CharField(widget=forms.PasswordInput)

	def __str__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError(f'Пользователь с ником {username} в системе не найден.')
		user = User.objects.filter(username=username).first()
		if user:
			if not user.check_password(password):
				raise forms.ValidationError("Неверный пароль")
		return self.cleaned_data

	class Meta:
		model = User
		fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
	confirm_password = forms.CharField(widget=forms.PasswordInput)
	password = forms.CharField(widget=forms.PasswordInput)
	phone = forms.CharField(required=False)

	def __str__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'
		self.fields['confirm_password'].label = 'Подтверждение пароля'
		self.fields['phone'].label = 'Номер телефона'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		if User.objects.filter(phone=phone).exists():
			raise forms.ValidationError(f'Данный номер телефона уже зарегистрирован в системе')
		return phone

	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError(f'Пользователь с логином {username} уже существует')
		return username

	def clean(self):
		password = self.cleaned_data['password']
		confirm_password = self.cleaned_data['confirm_password']
		if password != confirm_password:
			raise forms.ValidationError(f'Пароли не совпадают')
		return self.cleaned_data

	class Meta:
		model = User
		fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'phone']
