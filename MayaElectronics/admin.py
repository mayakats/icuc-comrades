from django.contrib import admin

from MayaElectronics.models import Department, User, ProductImages, Order, Cart, CartItem, Category, CustomUser, Feedback, Product

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)
    list_filter = ()
    search_fields = ('department_name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('department', 'salutation', 'fullname', 'gender', 'username', 'telephone', 'address', 'dob', 'marital_status', 'job_role')
    list_filter = ('dob',)
    search_fields = ('department_id', 'fullname')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('display_products', 'total_price', 'customer_name', 'quantity', 'email', 'address', 'telephone', 'created_at')
    list_filter = ()
    search_fields = ('phone_number', 'customer_name')

    def display_products(self, obj):
        return ', '.join([product.name for product in obj.products.all()])

    display_products.short_description = 'Products'

class ProductImageInline(admin.TabularInline):
    model = ProductImages
    max_num = 10
    min_num = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ]

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Feedback)
admin.site.register(Product, ProductAdmin)
