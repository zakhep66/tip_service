from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	id_branch = models.ForeignKey('Branch', related_name="id_branch", on_delete=models.CASCADE)
	card_number = models.CharField(verbose_name="Номер карты", max_length=20, null=True)

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

	class Meta:
		verbose_name = "Staff"
		verbose_name_plural = "Staffs"


class Payment(models.Model):
	staff = models.ForeignKey('Staff', related_name="staff", on_delete=models.CASCADE)
	sum_tea = models.IntegerField(verbose_name="Сумма чаевых")
	data = models.DateField(verbose_name="дата", auto_now_add=True)

	def __str__(self):
		return self.staff

	class Meta:
		verbose_name = "Сотрудник"
		verbose_name_plural = "Сотрудники"


class Organization(models.Model):
	legal_name = models.CharField(verbose_name="Юридическое имя", max_length=50)

	def __str__(self):
		return self.legal_name

	class Meta:
		verbose_name = "Юридическое имя"
		verbose_name_plural = "Юридические имена"


class Leader(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	id_organization = models.ForeignKey(Organization, related_name="id_organization", on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.last_name}, {self.first_name}'

	class Meta:
		verbose_name = "Leader"
		verbose_name_plural = "Leaders"


class Branch(models.Model):
	leader = models.ForeignKey(Staff, related_name="leader", on_delete=models.CASCADE)
	organization = models.ForeignKey('Organization', related_name="organization", on_delete=models.CASCADE)
	branch_name = models.CharField(verbose_name="Название филиала", max_length=30)
	address = models.CharField(verbose_name="Адресс", max_length=100)

	def __str__(self):
		return self.leader

	class Meta:
		verbose_name = "Филиал"
		verbose_name_plural = "Филиалы"
