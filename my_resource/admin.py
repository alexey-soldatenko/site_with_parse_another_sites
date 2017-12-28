from django.contrib import admin
from my_resource.models import URL_Parse, Parse_result

# Register your models here.
class URLAdmin(admin.ModelAdmin):
	list_display = ['url', 'minute', 'second']

class ResultAdmin(admin.ModelAdmin):
	list_display = ['url', 'status', 'date']

admin.site.register(URL_Parse, URLAdmin)
admin.site.register(Parse_result, ResultAdmin)