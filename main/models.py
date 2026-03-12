from django.db import models
import uuid
from django.utils import timezone

class AnonymousDesign(models.Model):
    # Unique ID for the visitor (stored in session)
    visitor_id = models.CharField(max_length=100, db_index=True)
    design_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Design Data
    name = models.CharField(max_length=255, default="My Custom Sign")
    design_json = models.TextField()  # Stores the Fabric.js JSON
    preview_image = models.ImageField(upload_to='design_previews/') # Real image file
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # This line MUST be indented with 4 spaces
        return f"Design {self.design_id} - Visitor {self.visitor_id[:8]}"
        

class CartItem(models.Model):
    # This identifies the unique browser without a login
    visitor_id = models.CharField(max_length=100, db_index=True, null=True)
    
    design_preview = models.ImageField(upload_to='custom_designs/')
    size = models.CharField(max_length=50)
    sides = models.CharField(max_length=20)
    material = models.CharField(max_length=50)
    finishing = models.CharField(max_length=50)
    mounting = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    
    # Pricing fields
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.id} - {self.visitor_id}"
        
        
class Order(models.Model):
    # Link to visitor
    visitor_id = models.CharField(max_length=100, db_index=True)
    
    # Contact Info
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Shipping Info
    ship_name = models.CharField(max_length=255)
    ship_address1 = models.CharField(max_length=255)
    ship_address2 = models.CharField(max_length=255, blank=True)
    ship_city = models.CharField(max_length=100)
    ship_state = models.CharField(max_length=100)
    ship_country = models.CharField(max_length=100)
    ship_zip = models.CharField(max_length=20)
    
    # Total
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.email}"
        
        
class GalleryImage(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='gallery/')
    uploaded_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title or f"Image {self.id}"