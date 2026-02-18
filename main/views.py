from django.shortcuts import render
from django.http import Http404 

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
        # Logic to handle form submission would go here
        pass
    return render(request, 'main/contact.html')