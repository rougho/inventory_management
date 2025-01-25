from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm
from .models import InventoryItem, Category
# from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages

class Index(TemplateView):
    template_name= 'inventory/index.html'

    def get(self, request):
        items = InventoryItem.objects.all().order_by('id')
        return render(request, self.template_name, {'items': items})

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
			# quantity__lte=LOW_QUANTITY
		)

		if low_inventory.count() > 0:
			if low_inventory.count() > 1:
				messages.error(request, f'{low_inventory.count()} items have low inventory')
			else:
				messages.error(request, f'{low_inventory.count()} item has low inventory')

		low_inventory_ids = InventoryItem.objects.filter(
			user=self.request.user.id,
			# quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

		return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})

