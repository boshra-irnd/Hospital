from django.contrib import admin
from django.utils.html import format_html, urlencode
from . import models
from django.urls import reverse
from django.db.models.aggregates import Count
from jalali_date import datetime2jalali, date2jalali
from jalali_date.admin import ModelAdminJalaliMixin, StackedInlineJalaliMixin, TabularInlineJalaliMixin	
 
    
@admin.register(models.Province)
class ProvinceAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ['name', 'get_updated_jalali', 'get_created_jalali','cities_count']
    search_fields = ['name']
    list_filter = ['update_date', 'create_date']
    list_per_page = 10
    
    def get_updated_jalali(self, obj):
 	    return datetime2jalali(obj.update_date).strftime('%y/%m/%d _ %H:%M:%S')
  
    def get_created_jalali(self, obj):
 	    return datetime2jalali(obj.create_date).strftime('%y/%m/%d _ %H:%M:%S')
  
    @admin.display(ordering='cities_count')
    def cities_count(self, province):
        url = (
            reverse('admin:management_system_city_changelist')
            + '?'
            + urlencode({
                'province__id': str(province.id)
            }))
        return format_html('<a href="{}">{}</a>', url, province.cities_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            cities_count=Count('cities')
        )


@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'province_name', 'person_count',
                    'get_updated_jalali', 'get_created_jalali']
    list_select_related = ['province']
    search_fields = ['name', 'province']
    list_select_related = ['province']
    list_filter = ['update_date', 'create_date']
    list_per_page = 10

    def province_name(self, city):
        return city.province.name
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(person_count=Count('person'))
    
    @admin.display(ordering='person_count')
    def person_count(self, city):
        return city.person_count
  
    def get_updated_jalali(self, obj):
 	    return datetime2jalali(obj.update_date).strftime('%y/%m/%d _ %H:%M:%S')
  
    def get_created_jalali(self, obj):
 	    return datetime2jalali(obj.create_date).strftime('%y/%m/%d _ %H:%M:%S')

