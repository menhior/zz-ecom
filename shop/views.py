from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Group
from django.db.models.query import EmptyQuerySet
import json
import datetime 

from django.forms import inlineformset_factory

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import *
from .forms import *
from .filters import *
from .utils import *
from .decorators import *
# Create your views here.

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    an_customer = data['an_customer']

    product_list = Product.objects.all()

    myFilter = ProductFilter(request.GET, queryset=product_list)
    product_list = myFilter.qs

    paginator = Paginator(product_list, 9)
    page = request.GET.get('page', 1)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'an_customer':  an_customer, 'products': products, 'cartItems': cartItems, 'myFilter': myFilter, 'paginator': paginator,}
    return render(request, 'shop/store.html', context)

def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    an_customer = data['an_customer']
 
    context = {'an_customer':  an_customer, 'items': items, 'order':order, 'cartItems': cartItems}
    return render(request, 'shop/cart.html', context)

def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    an_customer = data['an_customer']

    context = {'an_customer':  an_customer, 'items': items, 'order':order, 'cartItems': cartItems}
    return render(request, 'shop/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)


    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device, name = None)
    
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    print(created)
    print(order)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)    

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    customer_name = data['form']['name']
    customer_email = data['form']['email']

    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device, name = None)

        
    order, created = Order.objects.get_or_create(customer=customer, complete=False)    
    print(customer)
    print(order)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    print(order.transaction_id)

    if round(total, 2) == round(order.get_cart_total, 2):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment subbmitted..', safe=False)

def contactView(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == 'GET':
            form = CustomerContactForm()
        else:
            form = CustomerContactForm(request.POST)
            if form.is_valid():
                from_email = user.email
                subject = form.cleaned_data['subject']
                message = 'email: ' + from_email + '\n' + '\n' +"Message: " + form.cleaned_data['message']
                try:
                    send_mail(subject, message, from_email, ['menhior1@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')

                return redirect('success')

    else:
        if request.method == 'GET':
            form = ContactForm()
        else:
            form = ContactForm(request.POST)
            if form.is_valid():
                from_email = form.cleaned_data['Your_email']
                subject = form.cleaned_data['subject']
                message = 'email: ' + from_email + '\n' + '\n' +"Message: " + form.cleaned_data['message']
                try:
                    send_mail(subject, message, from_email, ['menhior1@gmail.com'])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('success')
    context = {'form': form}
    return render(request, 'shop/contact.html', context)



def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    customer = request.user.customer
    profile_picture = customer.profile_pic
    print(profile_picture)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.product = product
            form.save()
            return redirect('/product/' + str(pk) + '/')

    context = {'product': product, 'profile_picture': profile_picture,'form': form}
    return render(request, 'shop/product.html', context)

def about(request):
    context={}
    return render(request, 'shop/about.html')

def successView(request):
    return render(request, 'shop/contact_success.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password=password)


            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context  = {}
    return render(request, 'shop/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    """try:
        device = request.COOKIES['device']
        an_customer = 'Not_Nobody'

        if request.user.is_authenticated:
            return redirect('store')
        else:
            form = CreateUserForm()
            if request.method == 'POST':
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    Customer.objects.create(
                        user=user,
                        name=user.first_name + ' ' + user.last_name,
                        email = user.email,
                        device = device
                        )
                    group = Group.objects.get(name='customer')
                    user.groups.add(group)

                    username = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + username)

                    return redirect('login')
    except:
        an_customer = 'Nobody'
        form = CreateUserForm()"""

    device = request.COOKIES['device']
    an_customer = 'Not_Nobody'

    if request.user.is_authenticated:
        return redirect('store')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                Customer.objects.create(
                    user=user,
                    name=user.first_name + ' ' + user.last_name,
                    email = user.email,
                    device = device
                    )
                group = Group.objects.get(name='customer')
                user.groups.add(group)

                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + username)

                return redirect('login')

        context = {'form': form, 'an_customer': an_customer}
        return render(request, 'shop/register.html', context)

@login_required(login_url='login')
@admin_only
def dashboardView(request):
    orders = Order.objects.all().filter(complete=True).order_by('-date_ordered')

    customers = Customer.objects.all().order_by('-date_created')[:5]

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    orders_list = list(orders)[:5]
    context = {'orders':orders_list, 'customers':customers,
    'total_orders':total_orders,'delivered':delivered,
    'pending':pending }

    return render(request, 'shop/dashboard.html', context)

@login_required(login_url='login')
def userView(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        orders_list = customer.order_set.all().filter(complete=True)

        total_orders = orders_list.count()
        delivered = orders_list.filter(status='Delivered').count()
        pending = orders_list.filter(status='Pending').count()

        paginator = Paginator(orders_list, 5)
        page = request.GET.get('page', 1)

        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            orders = paginator.page(paginator.num_pages)

        context = {'orders':orders, 'total_orders':total_orders,
        'delivered':delivered,'pending':pending, 'paginator': paginator}
        return render(request, 'shop/user.html', context)
    else:
        return render(request, 'shop/login_required.html', {})

@login_required(login_url='login')
@admin_only
def orderList(request):
    orders_list = Order.objects.all().filter(complete=True).order_by('-date_ordered')

    myFilter = OrderListFilter(request.GET, queryset=orders_list)
    orders_list = myFilter.qs 

    paginator = Paginator(orders_list, 10)
    page = request.GET.get('page', 1)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {'orders': orders, 'myFilter': myFilter, 'paginator': paginator}
    return render(request, 'shop/order_list.html', context)

@login_required(login_url='login')
@admin_only
def customerList(request):
    customers_list = Customer.objects.all().order_by('-date_created')

    myFilter = CustomerListFilter(request.GET, queryset=customers_list)
    customers_list = myFilter.qs

    paginator = Paginator(customers_list, 10)
    page = request.GET.get('page', 1)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        customers = paginator.page(1)
    except EmptyPage:
        customers = paginator.page(paginator.num_pages)

    context = {'customers': customers, 'myFilter': myFilter}
    return render(request, 'shop/customer_list.html', context)

@login_required(login_url='login')
@admin_only
def orderItemList(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_item_list = order.orderitem_set.all()
    count = order.shippingaddress_set.all().count()
    if count != 0:
        shipping_address = order.shippingaddress_set.all().latest('date_added')
    else:
        shipping_address = None

    context = {'order': order, 'order_item_list': order_item_list, 'shipping_address': shipping_address, 'count': count}
    return render(request, 'shop/order_item_list.html', context)

@login_required(login_url='login')
@admin_only
def createOrder(request):
    form = FullOrderForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = FullOrderForm(request.POST)
        if form.is_valid():
            form.instance.complete =True
            order = form.save()
            if ShippingAddress.objects.all().filter(customer = order.customer).count() != 0:
                print(ShippingAddress.objects.all().filter(customer = order.customer).latest('date_added'))
                shipping_adress_for_order = ShippingAddress.objects.all().filter(customer = order.customer).latest('date_added')              
                print(shipping_adress_for_order.address)
                order.shippingaddress = ShippingAddress.objects.create(
                    customer=order.customer,
                    order=order,
                    address=shipping_adress_for_order.address,
                    city=shipping_adress_for_order.address,
                    state=shipping_adress_for_order.address,
                    zipcode=shipping_adress_for_order.address,
                    )
                return redirect('/dashboard/')
            else:
                return redirect('/dashboard/')
            """if ShippingAddress.objects.all().filter(customer = order.customer) != None:
                shipping_adress_for_order = ShippingAddress.objects.all().filter(customer = order.customer).latest('date_added')              
                order.shippingaddress = shipping_adress_for_order"""

                

    """OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')"""

    context = {'form':form,}
    return render(request, 'shop/order_create.html', context)

@login_required(login_url='login')
@admin_only
def updateOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = OrderForm(instance=order)
    print('ORDER:', order)
    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            user= request.user
            form.save()
            return redirect('/dashboard/')

    context = {'form':form}
    return render(request, 'shop/order_form.html', context)

@login_required(login_url='login')
@admin_only
def deleteOrder(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/dashboard/')

    context = {'item':order}
    return render(request, 'shop/delete.html', context)

@login_required(login_url='login')
@admin_only
def deleteCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('/dashboard/')

    context = {'item':customer}
    return render(request, 'shop/customer_delete.html', context)

@login_required(login_url='login')
@admin_only
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders_list = customer.order_set.all().filter(complete=True).order_by('-date_ordered')
    order_count = orders_list.count()

    myFilter = CustomerPageOrderFilter(request.GET, queryset=orders_list)
    orders_list = myFilter.qs

    shipping_address = customer.shippingaddress_set.all()

    paginator = Paginator(orders_list, 5)
    page = request.GET.get('page', 1)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {'customer':customer, 'orders':orders, 'order_count':order_count, 'shipping_address': shipping_address, 'myFilter': myFilter}
    return render(request, 'shop/customer.html',context)

@login_required(login_url='login')
@admin_only
def placeOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = FullOrderForm()
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        form = FullOrderForm(request.POST)
        if form.is_valid():
            form.instance.customer = customer
            form.instance.complete =True
            order = form.save()
            print(order)
            return redirect('/customer/' + str(pk))

    context = {'form':form}
    return render(request, 'shop/order_for_customer.html', context)

@login_required(login_url='login')
@admin_only
def updateCustomer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':

        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customer/' + str(pk))

    context = {'form':form}
    return render(request, 'shop/customer_update.html', context)

@login_required(login_url='login')
@admin_only
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')
                
    context = {'form':form,}
    return render(request, 'shop/customer_create.html', context)


@login_required(login_url='login')
@admin_only
def createOrderItems(request, order_pk):
    OrderFormSet = inlineformset_factory(Order, OrderItem, fields=('product', 'quantity'), extra=10 )
    order = get_object_or_404(Order, pk=order_pk)
    formset = OrderFormSet(queryset=OrderItem.objects.none(),instance=order)
    if request.method == 'POST':

        formset = OrderFormSet(request.POST, instance=order)
        if formset.is_valid():
            formset.save()
            return redirect('/order_item_list/' + str(order_pk))

    context = {'form':formset}
    return render(request, 'shop/create_order_items.html', context)

@login_required(login_url='login')
@admin_only
def deleteOrderItem(request, order_item_pk):
    order_item = get_object_or_404(OrderItem, pk=order_item_pk)
    if request.method == "POST":
        order_item.delete()
        return redirect('/dashboard/')

    context = {'item':order_item}
    return render(request, 'shop/order_item_delete.html', context)

@login_required(login_url='login')
@admin_only
def createShippingInformation(request, shipping_create_pk):
    order = get_object_or_404(Order, pk=shipping_create_pk)
    customer = order.customer
    form = ShippingAddressForm()
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.instance.customer = customer
            form.instance.order = order
            shipping = form.save()
            print(shipping.order)
            return redirect('/order_list/')

    context = {'form':form}
    return render(request, 'shop/shipping_create.html', context)


"""def placeOrder(request, pk):
    customer = Customer.objects.get(id=pk)
    form = FullOrderForm()
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        form = FullOrderForm(request.POST)
        if form.is_valid():
            form.instance.customer = customer
            form.instance.complete =True
            order = form.save()
            print(order)
            return redirect('/customer/' + str(pk))

    context = {'form':form}
    return render(request, 'shop/order_for_customer.html', context)"""

@login_required(login_url='login')
@admin_only
def updateShippingInformation(request, shipping_update_pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=shipping_update_pk)
    form = UpdateShippingForm(instance=shipping_address)
    if request.method == 'POST':

        form = UpdateShippingForm(request.POST, instance=shipping_address)
        if form.is_valid():
            form.save()
            return redirect('/order_list/')

    context = {'form':form}
    return render(request, 'shop/shipping_update.html', context)

@login_required(login_url='login')
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()


    context = {'form': form, 'customer': customer,}
    return render(request, 'shop/account_settings.html', context)


@login_required(login_url='login')
def customerOrderDetails(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order_item_list = order.orderitem_set.all()
    count = order.shippingaddress_set.all().count()
    if count != 0:
        shipping_address = order.shippingaddress_set.all().latest('date_added')
    else:
        shipping_address = None

    context = {'order': order, 'order_item_list': order_item_list, 'shipping_address': shipping_address, 'count': count}
    return render(request, 'shop/customer_order_details.html', context)
