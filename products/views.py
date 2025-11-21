from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction, IntegrityError, models
from django.contrib import messages 
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProductForm
from .models import Product , Category, Brand



def index(request):
    
    # Obtener productos destacados (máximo 8)
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category', 'brand')[:8]
    
    return render(request, 'index.html', {
        'featured_products': featured_products
    })

def is_staff_user(user):
    return user.is_staff


# ==============================================

# Gestión de Productos

# Lista de productos

def product_list(request):
    products = Product.objects.filter(is_active=True)
    
    # BÚSQUEDA (query de texto)
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(category__name__icontains=query) |
            models.Q(brand__name__icontains=query) |
            models.Q(sku__icontains=query)
        )
    
    # FILTRO: Categoría
    category_ids = request.GET.getlist('category')
    if category_ids:
        products = products.filter(category_id__in=category_ids)
    
    # FILTRO: Marca
    brand_ids = request.GET.getlist('brand')
    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)

    # FILTRO: Rango de precio
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # FILTRO: Solo en oferta
    if request.GET.get('featured') == '1':
        products = products.filter(is_featured=True)
        
    # FILTRO: Solo destacados
    if request.GET.get('featured') == '1':
        products = products.filter(is_featured=True)
    
    # FILTRO: Con stock
    if request.GET.get('in_stock') == '1':
        products = products.filter(stock__gt=0)
    
    # Aplicar select_related para optimizar
    products = products.select_related('category', 'brand').distinct()
    
    # Sorting

    sort = request.GET.get('sort', 'name')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'newest':
        products = products.order_by('-created_at')

    # Paginación
    paginator = Paginator(products, 12)  # 12 productos por página
    page = request.GET.get('page')
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        # Si page no es un entero, mostrar la primera página
        products_page = paginator.page(1)
    except EmptyPage:
        # Si page está fuera de rango, mostrar la última página
        products_page = paginator.page(paginator.num_pages)
    
    
    # Obtener datos para los filtros (sidebar)
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    
    # Calcular rango de precios
    price_range = Product.objects.filter(is_active=True).aggregate(
        min_price=models.Min('price'),
        max_price=models.Max('price')
    )
    
    # Mensajes
    if query and not products.exists():
        messages.info(request, f'No se encontraron productos para "{query}"')
    
    context = {
        'products': products_page,
        'query': query,
        'current_sort': sort,
        'total_results': paginator.count, 
        
        # Para filtros
        'categories': categories,
        'brands': brands,
        'price_range': price_range,
        
        # Filtros activos (para mantener estado)
        'selected_categories': category_ids,
        'selected_brands': brand_ids,
        'min_price': min_price,
        'max_price': max_price,
        'filter_on_sale': request.GET.get('on_sale'),
        'filter_featured': request.GET.get('featured'),
        'filter_in_stock': request.GET.get('in_stock'),

        # Paginación
        'paginator': paginator,
    }
    
    return render(request, 'products/product_list.html', context)


# Detalle del producto
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)

    ahorro = None
    if product.sale_price:
        ahorro = product.price - product.sale_price
    
    # Productos relacionados (misma categoría)
    related_products = None
    if product.category:
        related_products = Product.objects.filter(
            category=product.category,
            is_active=True
        ).exclude(pk=product.pk)[:4]
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'ahorro': ahorro
    })

# Crear nuevo producto

@login_required
@user_passes_test(is_staff_user)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) 

        if form.is_valid():
            try:
                with transaction.atomic():
                    producto = form.save()
                messages.success(request, 'Producto creado exitosamente.')
                return redirect('products:product_list')
            except IntegrityError:
                messages.error(request, 'Error al crear el producto. Inténtalo de nuevo.')

        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {'form': form})

# Editar producto existente
   
@login_required
@user_passes_test(is_staff_user)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Producto actualizado exitosamente.')
                return redirect('products:product_list')
            
            except IntegrityError:
                messages.error(request, 'Error al actualizar el producto. Inténtalo de nuevo.')

        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {'form': form, 'product': product})

# Eliminar producto (con confirmación)

@login_required
@user_passes_test(is_staff_user)
def product_confirm_delete(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('products:product_list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})

# ==============================================

def category_list(request):

    categories = Category.objects.filter(is_active=True).annotate(
        product_count=models.Count('products', filter=models.Q(products__is_active=True))
    )
    
    return render(request, 'products/category_list.html', {
        'categories': categories
    })


def category_detail(request, slug):

    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    # Obtener productos de la categoría
    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('brand')
    
    # Filtros
    # Marcas disponibles en esta categoría
    brands = Brand.objects.filter(
        products__category=category,
        products__is_active=True,
        is_active=True
    ).distinct()
    
    # Filtro: Marca
    brand_ids = request.GET.getlist('brand')
    if brand_ids:
        products = products.filter(brand_id__in=brand_ids)
    
    # Filtro: Precio
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Filtro: Opciones especiales
    if request.GET.get('on_sale') == '1':
        products = products.filter(sale_price__isnull=False)
    if request.GET.get('featured') == '1':
        products = products.filter(is_featured=True)
    if request.GET.get('in_stock') == '1':
        products = products.filter(stock__gt=0)
    
    # Sorting
    sort = request.GET.get('sort', 'name')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(products, 12)
    page = request.GET.get('page')
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    # Calcular rango de precios para esta categoría
    price_range = Product.objects.filter(
        category=category,
        is_active=True
    ).aggregate(
        min_price=models.Min('price'),
        max_price=models.Max('price')
    )
    
    context = {
        'category': category,
        'products': products_page,
        'brands': brands,
        'price_range': price_range,
        'current_sort': sort,
        'total_results': paginator.count,
        'paginator': paginator,
        
        # Filtros activos
        'selected_brands': brand_ids,
        'min_price': min_price,
        'max_price': max_price,
        'filter_on_sale': request.GET.get('on_sale'),
        'filter_featured': request.GET.get('featured'),
        'filter_in_stock': request.GET.get('in_stock'),
    }
    
    return render(request, 'products/category_detail.html', context)

# ==============================================

# Carrito de Compras

# Vista del carrito
def cart_view(request):

    cart = request.session.get('cart', {})                  # Obtener el carrito de la sesión
    products = Product.objects.filter(id__in=cart.keys())   # Obtener productos en el carrito
    cart_items = []                                         # Lista para almacenar items del carrito                                

    for product in products:
        quantity = cart[str(product.id)]                    # Cantidad del producto en el carrito          
        cart_items.append({                                 # Agregar item al carrito
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })

    total = sum(item['subtotal'] for item in cart_items)    # Calcular total del carrito

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total': total
    })



# Agregar producto al carrito

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    if str(product.id) in cart:                                                 # Si el producto ya está en el carrito
        cart[str(product.id)] += 1
    else:
        cart[str(product.id)] = 1

    request.session['cart'] = cart
    messages.success(request, f'Producto "{product.name}" agregado al carrito.')

    return redirect('products:lista_productos') 

# Agregar producto al carrito con cantidad especificada
def add_to_cart_with_quantity(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        cart = request.session.get('cart', {})
        
        quantity = int(request.POST.get('quantity', 1))
        
        # Validar que no exceda el stock
        if quantity > product.stock:
            messages.error(request, f'Solo hay {product.stock} unidades disponibles.')
            return redirect('products:detalle_producto', pk=pk)
        
        # Si ya existe en el carrito, sumar la cantidad
        if str(product.id) in cart:
            cart[str(product.id)] += quantity
        else:
            cart[str(product.id)] = quantity
        
        request.session['cart'] = cart
        messages.success(request, f'{quantity} unidad(es) de "{product.name}" agregadas al carrito.')
        
        return redirect('products:cart_view')
    
    return redirect('products:lista_productos')



# Eliminar producto del carrito 

def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})

    if str(product.id) in cart:
        del cart[str(product.id)]                       # Eliminar el producto del carrito
        request.session['cart'] = cart
        messages.success(request, f'Producto "{product.name}" eliminado del carrito.')
    else:
        messages.error(request, f'El producto "{product.name}" no está en el carrito.')

    return redirect('products:cart_view')



# Actualizar cantidad de un producto en el carrito

def update_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if quantity > 0:
            cart[str(product.id)] = quantity
            messages.success(request, f'Cantidad del producto "{product.name}" actualizada.')
        else:
            if str(product.id) in cart:
                del cart[str(product.id)]
                messages.success(request, f'Producto "{product.name}" eliminado del carrito.')

        request.session['cart'] = cart

    return redirect('products:cart_view')