from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Load sample categories and products into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading sample data...')

        # Categories
        categories_data = [
            {'name': 'Electronics',  'slug': 'electronics',  'icon': 'fas fa-laptop'},
            {'name': 'Clothing',     'slug': 'clothing',     'icon': 'fas fa-tshirt'},
            {'name': 'Books',        'slug': 'books',        'icon': 'fas fa-book'},
            {'name': 'Home & Kitchen','slug': 'home-kitchen','icon': 'fas fa-home'},
            {'name': 'Sports',       'slug': 'sports',       'icon': 'fas fa-football-ball'},
        ]

        cats = {}
        for c in categories_data:
            obj, created = Category.objects.get_or_create(slug=c['slug'], defaults={'name': c['name'], 'icon': c['icon']})
            cats[c['slug']] = obj
            if created:
                self.stdout.write(f'  Created category: {obj.name}')

        # Products
        products_data = [
            # Electronics
            {'name': 'Wireless Earbuds Pro',      'category': 'electronics', 'price': 2499, 'original_price': 3500, 'stock': 25, 'is_featured': True,  'rating': 4.7, 'description': 'Premium wireless earbuds with active noise cancellation, 30-hour battery life, and crystal-clear sound quality.'},
            {'name': 'Smart Watch Series 5',      'category': 'electronics', 'price': 5999, 'original_price': 8000, 'stock': 15, 'is_featured': True,  'rating': 4.5, 'description': 'Feature-rich smartwatch with health monitoring, GPS, and 7-day battery life. Compatible with Android and iOS.'},
            {'name': 'USB-C Fast Charger 65W',    'category': 'electronics', 'price': 899,  'original_price': 1200, 'stock': 50, 'is_featured': False, 'rating': 4.3, 'description': 'Super-fast 65W USB-C charger compatible with laptops, phones, and tablets. GaN technology for compact design.'},
            {'name': 'Bluetooth Speaker Mini',    'category': 'electronics', 'price': 1799, 'original_price': 2500, 'stock': 30, 'is_featured': False, 'rating': 4.6, 'description': 'Portable waterproof Bluetooth speaker with 360-degree surround sound and 12-hour playtime.'},

            # Clothing
            {'name': 'Classic Cotton T-Shirt',    'category': 'clothing',    'price': 599,  'original_price': 800,  'stock': 100,'is_featured': True,  'rating': 4.4, 'description': 'Premium 100% cotton t-shirt, available in multiple colors. Comfortable everyday wear with a modern fit.'},
            {'name': 'Slim Fit Jeans',            'category': 'clothing',    'price': 1899, 'original_price': 2500, 'stock': 40, 'is_featured': False, 'rating': 4.2, 'description': 'Stylish slim-fit jeans made from stretch denim for maximum comfort. Machine washable.'},
            {'name': 'Hoodie Sweatshirt',         'category': 'clothing',    'price': 1299, 'original_price': 1800, 'stock': 35, 'is_featured': True,  'rating': 4.8, 'description': 'Warm and cozy fleece hoodie perfect for casual outings. Available in multiple colours.'},

            # Books
            {'name': 'Python Programming Guide',  'category': 'books',       'price': 799,  'original_price': 999,  'stock': 20, 'is_featured': False, 'rating': 4.9, 'description': 'Comprehensive guide to Python programming from beginner to advanced level. Includes 200+ practical examples.'},
            {'name': 'Web Development Handbook',  'category': 'books',       'price': 899,  'original_price': 1200, 'stock': 18, 'is_featured': False, 'rating': 4.7, 'description': 'Complete reference for modern web development covering HTML, CSS, JavaScript, and popular frameworks.'},

            # Home & Kitchen
            {'name': 'Stainless Steel Water Bottle','category': 'home-kitchen','price': 699, 'original_price': 1000,'stock': 60, 'is_featured': True,  'rating': 4.5, 'description': 'Double-walled insulated water bottle keeps drinks cold 24hrs and hot 12hrs. BPA-free and eco-friendly.'},
            {'name': 'Non-Stick Cookware Set',    'category': 'home-kitchen','price': 3499, 'original_price': 5000, 'stock': 12, 'is_featured': False, 'rating': 4.3, 'description': '5-piece non-stick cookware set including fry pan, sauce pan, and stock pot. Dishwasher safe.'},

            # Sports
            {'name': 'Yoga Mat Premium',          'category': 'sports',      'price': 1299, 'original_price': 1800, 'stock': 25, 'is_featured': True,  'rating': 4.6, 'description': 'Extra thick 6mm yoga mat with non-slip surface and alignment lines. Includes carrying strap.'},
            {'name': 'Resistance Bands Set',      'category': 'sports',      'price': 799,  'original_price': 1100, 'stock': 45, 'is_featured': False, 'rating': 4.4, 'description': 'Set of 5 resistance bands with different tension levels. Perfect for home workouts and physiotherapy.'},
        ]

        for p in products_data:
            cat = cats.get(p['category'])
            obj, created = Product.objects.get_or_create(
                name=p['name'],
                defaults={
                    'category': cat,
                    'price': p['price'],
                    'original_price': p['original_price'],
                    'stock': p['stock'],
                    'is_featured': p['is_featured'],
                    'rating': p['rating'],
                    'description': p['description'],
                }
            )
            if created:
                self.stdout.write(f'  Created product: {obj.name}')

        self.stdout.write(self.style.SUCCESS('\nSample data loaded successfully!'))
        self.stdout.write(f'  Categories: {Category.objects.count()}')
        self.stdout.write(f'  Products:   {Product.objects.count()}')
