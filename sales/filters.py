from .models import SalesReceipt
import django_filters


class SalesFilter(django_filters.FilterSet):
    date_created = django_filters.DateFilter(
        field_name='sale_date'
    )

    class Meta:
        model = SalesReceipt
        fields = ['date_created']
