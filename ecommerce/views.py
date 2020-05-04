from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.models import User
from .models import *
from .forms import CheckoutForm
import stripe

stripe.api_key = "sk_test_5qrilYpoZYzC1B4NDBSxkysy004KrgIebV"

class HomeView(ListView):
    model = Item
    paginate_by = 3 
    template_name = "theplaza/index.html"

class ProductDetailView(DetailView):
    model = Item
    template_name = "theplaza/product.html"

class CartView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':order
            }
            return render(self.request, 'theplaza/cart.html', context)
        except ObjectDoesNotExist:
            messages.success(self.request, 'Please Add Something To Your Cart First!')
            return redirect('ecommerce:home')

@login_required
def add_to_cart(request, slug, pk):
    item = get_object_or_404(Item, slug=slug, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(item__slug=item.slug, item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Item added')
            return redirect('ecommerce:cart')
        
        else:
            order.item.add(order_item)
            messages.info(request, 'Item added to cart')
            return redirect('ecommerce:cart')
            
    else:
        order = Order.objects.create(
            user=request.user,
        )
        order.item.add(order_item)
        messages.info(request, 'Item added to cart')
        return redirect('ecommerce:product', slug=slug, pk=pk)

@login_required
def remove_from_cart(request, slug, pk):
    item = get_object_or_404(Item, slug=slug, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(item__slug=item.slug, item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.item.remove(order_item)
            order_item.quantity = 1
            order_item.save()
            order.save()
            messages.info(request, 'Item removed Sucessfully!')
            return redirect('ecommerce:cart')
        
        else:
            messages.info(request, 'You do not have this item in the order')
            return redirect('ecommerce:product', slug=slug, pk=pk)

    else:
        messages.info(request, 'You do not have any orders.')
        return redirect('ecommerce:product', slug=slug, pk=pk)

@login_required
def remove_one_from_cart(request, slug, pk):
    item = get_object_or_404(Item, slug=slug, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]

        if order.item.filter(item__slug=item.slug, item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, 'Item Quantity decreased!')
            else:
                order.item.remove(order_item)
                order.save()
                messages.info(request, 'Item removed Sucessfully!')
            return redirect('ecommerce:cart')

class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request, 'theplaza/checkout.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                address = form.cleaned_data.get('address')
                zip = form.cleaned_data.get('zip')
                payment_option = form.cleaned_data.get('payment_option')
                save_info = form.cleaned_data.get('save_info')
                order.save()
                if payment_option == 'S':
                    return redirect('ecommerce:payment', payment_option)
                else:
                    return redirect('/')
            messages.warning(self.request, 'Invalid form')
            return redirect('ecommerce:home')
        except ObjectDoesNotExist:
            messages.success(self.request, 'Please Add Something To Your Cart First!')
            return redirect('ecommerce:home')

class PaymentView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
            return render(self.request, 'theplaza/payment.html')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        amount = int(order.get_final_price() * 100)
        email='Biu@gmail.com'
        address='address'
        name=order.user.first_name
        customer = stripe.Customer.create(
                address={
                    'line1': address,
                },
                email=email,
                name=name,
                source=self.request.POST['stripeToken']
            )

            #Accepting Payments

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount,
            currency='usd',
            description="Total Price"
        )

        payment = Payment()
        payment.stripe_charge_id = charge['id']
        payment.user = self.request.user
        payment.amount = amount


        order.ordered = True
        order.save()

        return redirect('/')

def error_404_view(request, exception):
    data = {"name": "ThePythonDjango.com"}
    return render(request,'theplaza/error_404.html', data)