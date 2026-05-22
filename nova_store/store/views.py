from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm


def get_or_create_cart(request):
    """Get or create a cart for the current user or session."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart


def home_view(request):
    """Homepage: featured products + all products with category filter."""
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search', '')

    products = Product.objects.filter(stock__gt=0)

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if search_query:
        products = products.filter(name__icontains=search_query)

    featured_products = Product.objects.filter(is_featured=True, stock__gt=0)[:4]

    context = {
        'products': products,
        'categories': categories,
        'featured_products': featured_products,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'store/home.html', context)


def product_detail_view(request, product_id):
    """Single product detail page."""
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product_id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def category_view(request, slug):
    """All products in a category."""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, stock__gt=0)
    categories = Category.objects.all()

    context = {
        'category': category,
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/category.html', context)


def cart_view(request):
    """Show the shopping cart."""
    cart = get_or_create_cart(request)
    shipping = 0 if cart.total_price >= 2000 else 150
    grand_total = cart.total_price + shipping
    context = {
        'cart': cart,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


def add_to_cart_view(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Product, id=product_id)

    if not product.is_in_stock:
        messages.error(request, f'Sorry, {product.name} is out of stock.')
        return redirect('store:product_detail', product_id=product_id)

    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f'{product.name} added to your cart!')
    return redirect(request.META.get('HTTP_REFERER', 'store:home'))


def remove_from_cart_view(request, item_id):
    """Remove an item from the cart."""
    item = get_object_or_404(CartItem, id=item_id)
    product_name = item.product.name
    item.delete()
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('store:cart')


def update_cart_view(request, item_id):
    """Update quantity of a cart item."""
    item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        item.delete()
        messages.success(request, 'Item removed from cart.')
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, 'Cart updated.')

    return redirect('store:cart')


@login_required
def checkout_view(request):
    """Checkout page — collect shipping info and place order."""
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('store:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.total_price
            order.save()

            # Transfer cart items to order items
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                # Reduce stock
                item.product.stock -= item.quantity
                item.product.save()

            # Clear the cart
            cart.items.all().delete()

            messages.success(request, 'Order placed successfully! Thank you.')
            return redirect('store:order_confirmation', order_id=order.id)
    else:
        # Pre-fill form with user data
        initial = {
            'full_name': f'{request.user.first_name} {request.user.last_name}'.strip() or request.user.username,
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial)

    shipping = 0 if cart.total_price >= 2000 else 150
    grand_total = cart.total_price + shipping
    context = {
        'form': form,
        'cart': cart,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def order_confirmation_view(request, order_id):
    """Order success page."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def my_orders_view(request):
    """List all orders for the logged-in user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})
