from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404 
import json
import uuid
import base64
from django.core.files.base import ContentFile
from .models import AnonymousDesign, CartItem, Order, GalleryImage 
from datetime import datetime, timedelta
from django.http import Http404, JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,"main/index.html")

# Move your dictionary outside the function so both views can use it
PRODUCTS_DATA = {
    'led-message-signs': {
        'title': 'LED Electronic Message Signs',
        'subtitle': 'Digital Communication',
        'desc': 'High-impact, programmable LED displays designed for maximum daylight visibility and 24/7 engagement.',
        'features': ['Weatherproof Rating', 'Wi-Fi Control', 'Ultra-Bright Nits', 'Custom Sizes'],
        'icon': 'fa-bolt',
        'spec': 'P10/P6 Resolution'
    },
    'custom-t-shirts': {
        'title': 'Custom Apparel & Workwear',
        'subtitle': 'Brand Identity',
        'desc': 'Premium garment printing using UV-cured inks that last through 100+ washes without fading or cracking.',
        'features': ['No Minimums', 'UV-Cured Inks', 'Polyester & Cotton', 'Retail Finish'],
        'icon': 'fa-tshirt',
        'spec': 'High-Fidelity Print'
    },
    'vehicle-wraps': {
        'title': 'Fleet & Vehicle Branding',
        'subtitle': 'Mobile Advertising',
        'desc': 'Transform your company vehicles into 24/7 mobile billboards with our 3M certified vinyl wrapping.',
        'features': ['3M Certified Vinyl', 'UV Protection Layer', 'Full & Partial Wraps', 'No Residue Removal'],
        'icon': 'fa-truck-moving',
        'spec': '5-Year Warranty'
    },
    'architectural-signs': {
        'title': 'Architectural Signage',
        'subtitle': 'Building Identity',
        'desc': 'Dimensional letters and monument signs that define your professional space with elegance and durability.',
        'features': ['Aluminum/Acrylic', 'Backlit Options', 'Precision CNC Cut', 'Site Installation'],
        'icon': 'fa-building',
        'spec': 'Industrial Grade'
    },
}

def all_products(request):
    # This view shows EVERY product
    return render(request, 'main/products_list.html', {'products': PRODUCTS_DATA})

def product_detail(request, product_slug):
    # This view shows ONE specific product
    product = PRODUCTS_DATA.get(product_slug)
    if not product:
        raise Http404("Product does not exist")
    return render(request, 'main/product_detail.html', {'product': product})

def services(request):
    services_list = [
        {
            'title': 'Sign Design',
            'desc': 'Our graphic designers specialize in high-visibility branding and professional layouts tailored for signage.',
            'icon': 'fa-pen-nib'
        },
        {
            'title': 'Professional Installation',
            'desc': 'From bucket truck services to indoor mounting, our team ensures your signs are installed safely and securely.',
            'icon': 'fa-tools'
        },
        {
            'title': 'Wide Format Printing',
            'desc': 'Using state-of-the-art printers and UV-resistant inks for massive, high-detail banners and wraps.',
            'icon': 'fa-print'
        },
        {
            'title': 'Laser Engraving',
            'desc': 'Precision engraving on wood, acrylic, and metal for personalized products and industrial plaques.',
            'icon': 'fa-microchip'
        },
        {
            'title': 'Special Financing',
            'desc': 'We offer flexible financing options to help your business get the signage it needs today.',
            'icon': 'fa-file-invoice-dollar'
        }
    ]
    return render(request, 'main/services.html', {'services': services_list})

def material(request):
    materials_list = [
        {'name': 'Acrylic', 'desc': 'Glass-like finish, perfect for high-end indoor/outdoor logos.'},
        {'name': 'Aluminum', 'desc': 'Ultra-durable and rust-proof. Ideal for long-term exterior signs.'},
        {'name': 'Coroplast', 'desc': 'Lightweight and waterproof. The gold standard for yard signs.'},
        {'name': 'PolyMetal', 'desc': 'Strong aluminum faces with a plastic core. Best for rigid building signs.'},
        {'name': 'Vinyl', 'desc': 'Flexible and vibrant. Used for banners, decals, and vehicle wraps.'},
        {'name': 'HDU Board', 'desc': 'High-Density Urethane. Perfect for carved, dimensional artisan signs.'},
        {'name': 'PVC / Plastic', 'desc': 'Smooth finish, great for directional and menu boards.'},
        {'name': 'Poly Carbonate', 'desc': 'Virtually unbreakable. Used for illuminated sign faces.'},
    ]
    return render(request, 'main/materials.html', {'materials': materials_list})

def contact(request):
    if request.method == "POST":
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        interested_in = request.POST.get('interested_in')
        message = request.POST.get('message')

        # Email subject and body
        subject_admin = f"New Contact Form Submission - Accutech Sign Shop"
        message_admin = f"""
Name: {full_name}
Email: {email}
Interested In: {interested_in}
Message: {message}
"""  # Removed 'Company: Accutech Sign Shop' line for admin

        subject_user = f"Thank you for contacting Accutech Sign Shop"
        message_user = f"""
Hi {full_name},

Thank you for reaching out to Accutech Sign Shop! We received your message:

{message}

We will get back to you shortly.

– Accutech Sign Shop
"""

        # Send email to admin(s)
        admin_list = settings.ADMIN_EMAIL.split(',')  # Split multiple admins
        send_mail(
            subject_admin,
            message_admin,
            settings.DEFAULT_FROM_EMAIL,
            admin_list,
            fail_silently=False,
        )

        # Send confirmation email to user
        send_mail(
            subject_user,
            message_user,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return render(request, 'main/contact.html')

    return render(request, 'main/contact.html')
    
def scratch_page(request):
    # Ensure the visitor has a unique session ID
    if not request.session.session_key:
        request.session.create()
    return render(request, "main/scratch.html")

def save_design_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            visitor_id = request.session.session_key
            
            # 1. Handle the Base64 Image string from Canvas
            format, imgstr = data['preview'].split(';base64,') 
            ext = format.split('/')[-1] 
            image_data = ContentFile(base64.b64decode(imgstr), name=f"design_{uuid.uuid4()}.{ext}")

            # 2. Save to Database
            design = AnonymousDesign.objects.create(
                visitor_id=visitor_id,
                design_json=data['design_json'],
                preview_image=image_data
            )

            return JsonResponse({
                'status': 'success', 
                'message': 'Design saved to your session!',
                'design_id': str(design.design_id)
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'invalid_method'}, status=405)

def configure_sign(request):
    """
    Renders the configuration page. 
    Expects design_data (Base64) from the scratch editor.
    """
    design_data = request.POST.get('design_data', '')
    
    if not design_data:
        # If user refreshes or hits the page without data, send them back
        return redirect('design_scratch')

    context = {
        'design_data': design_data,
    }
    return render(request, 'main/configure_sign.html', context)

def add_to_cart(request):
    if request.method == "POST":
        # --- FIX 1: VISITOR TRACKING ---
        # Get ID from cookie or session to keep the cart private to this browser
        v_id = request.COOKIES.get('visitor_uuid') or str(uuid.uuid4())

        # 1. Capture Metadata
        size = request.POST.get('size')
        sides = request.POST.get('sides')
        material = request.POST.get('material')
        finishing = request.POST.get('finishing')
        mounting = request.POST.get('mounting')
        quantity = int(request.POST.get('quantity', 1))

        # --- FIX 2: REMOVE COMMAS ---
        # Removed the commas that caused the "tuple" ValidationError
        unit_price = 15.00
        total_price = unit_price * quantity
        
        # 2. Process Image
        design_data = request.POST.get('design_data')
        if design_data and "base64," in design_data:
            header, imgstr = design_data.split('base64,')
            ext = header.split('/')[-1].split(';')[0]
            filename = f"custom_sign_{uuid.uuid4()}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=filename)
        else:
            image_file = None

        # 3. Save to Database
        CartItem.objects.create(
            visitor_id=v_id,  # Assigning the ID here
            design_preview=image_file,
            size=size,
            sides=sides,
            material=material,
            finishing=finishing,
            mounting=mounting,
            quantity=quantity,
            unit_price=unit_price,
            total_price=total_price
        )
        
        response = redirect('cart_page')
        # Set the cookie so the user keeps their cart for 30 days
        response.set_cookie('visitor_uuid', v_id, max_age=2592000)
        return response

    return redirect('scratch')

def cart_page(request):
    # Only fetch items belonging to THIS visitor
    v_id = request.COOKIES.get('visitor_uuid')
    if v_id:
        items = CartItem.objects.filter(visitor_id=v_id).order_by('-created_at')
    else:
        items = CartItem.objects.none()

    cart_total = sum(item.total_price for item in items)
    
    return render(request, 'main/cart_page.html', {
        'items': items,
        'cart_total': cart_total
    })

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_page')
    
def checkout(request):
    v_id = request.COOKIES.get('visitor_uuid')
    items = CartItem.objects.filter(visitor_id=v_id)
    cart_total = sum(item.total_price for item in items)

    if not items:
        return redirect('cart_page')

    if request.method == "POST":
        # Capture form data and save Order here (Logic for payment follows)
        return redirect('secure_checkout') # Redirect to PayPal

    return render(request, 'main/checkout.html', {
        'items': items,
        'cart_total': cart_total
    })

def final_checkout(request):
    v_id = request.COOKIES.get('visitor_uuid')
    items = CartItem.objects.filter(visitor_id=v_id)
    
    # Pricing logic
    cart_total = sum(item.total_price for item in items)
    savings = 197.50  # Example savings
    tax = 19.11
    
    # Calculate dynamic dates (Business days)
    today = datetime.now()
    dates = {
        'economy': (today + timedelta(days=12)).strftime('%m/%d/%Y'),
        'standard': (today + timedelta(days=8)).strftime('%m/%d/%Y'),
        'rush': (today + timedelta(days=7)).strftime('%m/%d/%Y'),
    }

    return render(request, 'main/secure_checkout.html', {
        'items': items,
        'cart_total': cart_total,
        'savings': savings,
        'tax': tax,
        'dates': dates,
        'user_info': {
            'name': 'John Dae',
            'address': '123 Main St, Phoenix, AZ 85001, USA'
        }
    })

def payment_success(request):
    # Get the visitor ID to find their specific cart
    v_id = request.COOKIES.get('visitor_uuid')
    
    # Optional: Logic to save these items into a permanent 'Order' model before deleting
    # For now, we clear the cart
    CartItem.objects.filter(visitor_id=v_id).delete()

    # We recreate the context data needed for the success page display
    today = datetime.now()
    context = {
        'user_info': {
            'name': 'Valued Customer',  # In a real app, pull this from the saved Order model
            'address': 'Your shipping address'
        },
        'dates': {
            'standard': (today + timedelta(days=8)).strftime('%m/%d/%Y'),
        }
    }
    
    return render(request, 'main/success.html', context)
    
def gallery(request):
    images = GalleryImage.objects.order_by('-uploaded_at')  # newest first
    return render(request, 'main/gallery.html', {'images': images})