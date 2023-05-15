from django_filters import FilterSet, ModelChoiceFilter, DateFilter
from .models import Post, Category
from django import forms


class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Класс',
        empty_label='Все классы'
    )
    create_time = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                             lookup_expr='gt',
                             label='Дата публикации')


class ResponsesFilter(FilterSet):
    post = ModelChoiceFilter(
        queryset=Post.objects.all(),
        label='Объявление',
        empty_label='Все объявления',
        method='filter_listing',
    )

    create_time = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                             lookup_expr='gt',
                             label='Дата публикации')
