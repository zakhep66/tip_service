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
