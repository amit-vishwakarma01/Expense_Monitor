from django.contrib import admin
from.models import expense_detail,expense_type,query,replies
# Register your models here.
admin.site.register(expense_detail)
admin.site.register(expense_type)
admin.site.register(query)
admin.site.register(replies)