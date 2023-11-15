from django.contrib import admin
from .models import Category, Product, Discount, Homepage, Event
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product','discount_percentage','discounted_price', 'start_date', 'end_date', 'active')
    readonly_fields = ['discounted_price', 'active'] 
    
class DiscountInline(admin.TabularInline):
    model = Discount  
    fields = ['discount_percentage','start_date', 'end_date','discounted_price']
    readonly_fields = ['discounted_price',] 
    extra = 1
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'initial_price', 'display_categories', 'thumbnail')
    list_filter = ('categories', 'name')
    search_fields = ('name', 'description')
    change_form_template = 'admin/discount_form.html'
    fields = ['name', 'categories', 'description', 'thumbnail', 'thumbnail_title','initial_price']
    inlines = [DiscountInline]  

    def display_categories(self, obj):
            return",".join([category.name for category in obj.categories.all()])
        
@admin.register(Homepage)
class Homepage(admin.ModelAdmin):
    list_display = ('name', 'text','image', 'active')

@admin.register(Event)
class Event(admin.ModelAdmin):
    list_display = ('name', 'text','image', 'active')