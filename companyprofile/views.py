from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from .models import Company
from mauzo.decorators import allowed_user


# Create your views here.


def home(request):
    home_context = 'home'
    context = {
        'home_context': home_context
    }
    return render(
        request, 'home/home.html', context
    )


class CompanyCreate(CreateView):
    model = Company
    fields = [
        'company_name', 'postal_address',
        'telephone_1', 'telephone_2',
        'kra_pin', 'kra_vat',
    ]

    def form_valid(self, form):
        return super(CompanyCreate, self).form_valid(form)
