from django.db import models


class Common(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Province(Common):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
    
    
class City(Common):
    name = models.CharField(max_length=255)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, related_name='cities')
    
    def __str__(self):
        return (f'{self.name} | {self.province}')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'cities'


class Person(Common):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.IntegerField()
    certificate_code = models.IntegerField()
    birth_date = models.DateField()
    province = models.ForeignKey(Province, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    
class PhoneNumber(Common):
    phone_number = models.CharField(max_length=11)
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.phone_number
    
    class Meta:
        ordering = ['phone_number']
    
    
class Document(Common):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    primary_cause_of_the_disease = models.CharField(max_length=255)
    fish_amount = models.PositiveIntegerField()
    franchise = models.IntegerField()
    hospitalization_date = models.DateTimeField()
    release_date = models.DateTimeField()
    
    def __str__(self):
        return self.primary_cause_of_the_disease
    
    class Meta:
        ordering = ['hospitalization_date', 'release_date', 'primary_cause_of_the_disease']
