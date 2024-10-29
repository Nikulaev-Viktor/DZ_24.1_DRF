from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name')
    search_fields = ('email', 'first_name')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paid_lesson', 'paid_course', 'amount', 'payment_method')
    search_fields = ('user', 'paid_lesson', 'paid_course', 'amount')
    list_filter = ('payment_method',)
