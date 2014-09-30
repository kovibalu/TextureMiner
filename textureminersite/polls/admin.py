from django.contrib import admin

from models import AnnotatedImage
from models import SubImage
from models import FeatureVector


# Register your models here.
class AnnotatedImageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Naming information', {'fields': ['name', 'path']}),
        ('Date information', {'fields': ['comp_date']}),
        ('Other', {'fields': ['ratio']}),
    ]
    list_display = ('name', 'path', 'comp_date')
    list_filter = ['comp_date']
    search_fields = ['name']

admin.site.register(AnnotatedImage, AnnotatedImageAdmin)
admin.site.register(SubImage)
admin.site.register(FeatureVector)