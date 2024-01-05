from django.contrib import admin
from.models import Pod_detail,pod_member,Pod_transaction
# Register your models here.
admin.site.register(Pod_transaction)
admin.site.register(pod_member)
admin.site.register(Pod_detail)
