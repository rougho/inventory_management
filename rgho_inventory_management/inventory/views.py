from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category
from rgho_inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q


class Index(TemplateView):
    template_name= 'inventory/index.html'

    def get(self, request):
        items = InventoryItem.objects.all().order_by('id')
        low_inventory = InventoryItem.objects.filter(
			quantity__lte=LOW_QUANTITY
		)

        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'{low_inventory.count()} items have low inventory')
            else:
                messages.error(request, f'{low_inventory.count()} item has low inventory')
                
        low_inventory_ids = InventoryItem.objects.filter(
            quantity__lte=LOW_QUANTITY
        ).values_list('id', flat=True)
                
        return render(request, self.template_name, {'items': items, 'low_inventory_ids': low_inventory_ids})


class Navbar(TemplateView):
    template_name = 'inventory/navbar.html'
    
    def get(self, request):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})


class SignUp(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form':form})
    
    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user=authenticate(
                username=form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )

            login(request, user)
            return redirect('index')
        return render(request, 'inventory/signup.html', {'form':form})
    

class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		items = InventoryItem.objects.filter(user=self.request.user.id).order_by('id')

		low_inventory = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		)

		if low_inventory.count() > 0:
			if low_inventory.count() > 1:
				messages.error(request, f'{low_inventory.count()} items have low inventory')
			else:
				messages.error(request, f'{low_inventory.count()} item has low inventory')

		low_inventory_ids = InventoryItem.objects.filter(
			user=self.request.user.id,
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

		return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})


class AddItem(LoginRequiredMixin, CreateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)
      

class SearchInventory(View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        items = InventoryItem.objects.all()
        if search_query:
            items = items.filter(
                Q(product__icontains=search_query) | Q(category__name__icontains=search_query)
            )
        if request.user.is_authenticated:
            items = items.filter(user=request.user)
        items = items.order_by('id')
        return render(request, 'inventory/index.html', {
            'items': items,
            'search_query': search_query
        })


class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('dashboard')
	context_object_name = 'item'

def category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = InventoryItem.objects.filter(category=category).order_by('id')

    return render(request, 'inventory/index.html', {
        'items': items,
        'category': category,
    })