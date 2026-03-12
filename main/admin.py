from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import AnonymousDesign, GalleryImage
from django.utils.html import mark_safe

@admin.register(AnonymousDesign)
class AnonymousDesignAdmin(admin.ModelAdmin):
    # What you see in the main list
    list_display = ('design_id', 'visitor_id', 'preview_thumbnail', 'created_at')
    
    # What you see when you click into a specific design
    readonly_fields = ('preview_thumbnail_large', 'design_json', 'visitor_id', 'created_at')
    
    # Exclude the raw file field since we are showing the thumbnail
    fields = ('visitor_id', 'name', 'preview_thumbnail_large', 'design_json', 'created_at')

    def preview_thumbnail(self, obj):
        if obj.preview_image:
            return mark_safe(f'<img src="{obj.preview_image.url}" style="width: 80px; height: auto; border-radius: 4px; border: 1px solid #ddd;" />')
        return "No Image"
    preview_thumbnail.short_description = "Preview"

    def preview_thumbnail_large(self, obj):
        if obj.preview_image:
            return mark_safe(f'<img src="{obj.preview_image.url}" style="max-width: 600px; height: auto; border: 2px solid #ccc;" />')
        return "No Image"
    preview_thumbnail_large.short_description = "Full Design View"
    
    
    
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'thumbnail', 'uploaded_at')
    readonly_fields = ('thumbnail',)

    def thumbnail(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width:100px; height:auto; border-radius:5px;" />')
        return "No Image"
    thumbnail.short_description = "Thumbnail"