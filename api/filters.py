import django_filters
from .models import Member


class MemberFilter(django_filters.FilterSet):
    """
    Filter class for proving filter options with from, to date and status fields.
    """
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    status = django_filters.NumberFilter(field_name='status')

    class Meta:
        model = Member
        fields = ['created_after', 'created_before', 'status']
