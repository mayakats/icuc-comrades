from django.contrib import admin

from MayaElectronics.models import Department, User,  Order, Cart, CartItem, Category, CustomUser, Feedback, Product

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_name',)
    list_filter = ()
    search_fields = ('department_name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','department', 'salutation', 'fullname', 'gender', 'username', 'telephone', 'address', 'dob', 'marital_status', 'job_role')
    list_filter = ('dob',)
    search_fields = ('department_id', 'fullname')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'total_price', 'customer_name', 'quantity', 'email', 'address', 'telephone', 'created_at')

class ProductAdmin(admin.ModelAdmin):
   list_display = ('name', 'price', 'category', 'title', 'description', 'quantity', 'available')

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(CustomUser)
admin.site.register(Feedback)
admin.site.register(Product, ProductAdmin)
