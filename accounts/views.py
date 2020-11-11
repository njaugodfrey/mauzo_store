from django.shortcuts import render

# Create your views here.


def accounts_index(request):
    return render(
        request, template_name='accounts/accounts_index.html'
    )
