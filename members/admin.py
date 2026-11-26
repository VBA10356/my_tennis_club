from django.contrib import admin
from .models import Member

# Register your models here.

#We can also make changeslike this 
class MemberAdmin(admin.ModelAdmin):
      list_display = ("firstName", "lastName", "slug")
      prepopulated_fields = {"slug": ("firstName", "lastName")}



admin.site.register(Member, MemberAdmin)


