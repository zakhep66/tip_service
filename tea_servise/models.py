from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=20)
	id_branch = models.ForeignKey('Branch', related_name="id_branch", on_delete=models.CASCADE)
	card_number = models.CharField(verbose_name="Номер карты", max_length=20, null=True)
	avatar = models.ImageField(verbose_name="Аватар", null=True, blank=True)

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

	class Meta:
		verbose_name = "Сотрудник"
		verbose_name_plural = "Сотрудники"


class Payment(models.Model):
	STAR = (
		(1, 'единица'),
		(2, 'двойка'),
		(3, 'тройка'),
		(4, 'четвёрка'),
		(5, 'пятёрка')
	)
	staff = models.ForeignKey(Staff, related_name="staff", on_delete=models.CASCADE)
	sum_tea = models.IntegerField(verbose_name="Сумма чаевых")
	data = models.DateField(verbose_name="дата", auto_now_add=True)
	rating = models.IntegerField(verbose_name="Рейтинг", choices=STAR, null=True)
	review = models.TextField(verbose_name="Отзыв о сотруднике", null=True)

	def __str__(self):
		return self.staff.first_name

	class Meta:
		verbose_name = "Чаевые"
		verbose_name_plural = "Чаевые"


class Organization(models.Model):
	legal_name = models.CharField(verbose_name="Юридическое имя", max_length=50)

	def __str__(self):
		return self.legal_name

	class Meta:
		verbose_name = "Юридическое имя"
		verbose_name_plural = "Юридические имена"


class Leader(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20, verbose_name="Номер телефона", null=True)
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=20)

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

	class Meta:
		verbose_name = "Руководитель"
		verbose_name_plural = "Руководители"


class Branch(models.Model):
	leader = models.ForeignKey(Leader, related_name="leader", on_delete=models.CASCADE)
	organization = models.ForeignKey(Organization, related_name="organization", on_delete=models.CASCADE)
	branch_name = models.CharField(verbose_name="Название филиала", max_length=30)
	address = models.CharField(verbose_name="Адрес", max_length=100)

	def __str__(self):
		return self.branch_name

	class Meta:
		verbose_name = "Филиал"
		verbose_name_plural = "Филиалы"
