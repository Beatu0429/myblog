from django_filters import rest_framework as filters
from .models import Post

class MyFilter(filters.FilterSet):
    my_field = filters.CharFilter(
        lookup_expr='icontains',
        label='My Field',
        template='django_filters/rest_framework/multiple_choice_filter.html'
    )

    class Meta:
        model = Post
        fields = ['my_field']

    queryset = Post.objects.all()
