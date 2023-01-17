from django.contrib import admin
from realty.models import ObjectCategory, Objects, Images
from django.utils.translation import gettext_lazy as _

# Register your models here.
class ImagesInline(admin.TabularInline):
    model = Images
class ObjectsAdmin(admin.ModelAdmin):
    ordering = ('-updated_at',)
    inlines = [ImagesInline]
    list_display = ('category', 'manager', 'title')
    list_filter = ['category', 'manager']
    search_fields = ('title','residence','construction_company')
    fieldsets = (
        (_('Общее'), {
            'fields': ('title','locate','document','price','manager','category',)
        }),
        (_('Относительно жилого помещения'), {
            'fields': ('residence','construction_company','year','qty_room','area','floor','repair',
                       'wall_material','additional_buildings','communications','is_separately',
                       ),
        }),
        (_('Относительно участка'), {
            'classes': ('collapse',),
            'fields': ('land_area','appointment','lenght_width'),
        }),
    )


admin.site.register(ObjectCategory)
admin.site.register(Objects,ObjectsAdmin)
# admin.site.register(Objects)
admin.site.register(Images)
