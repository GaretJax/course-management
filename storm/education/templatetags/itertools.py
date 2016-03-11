from django import template


register = template.Library()


@register.filter('range')
def range_over(val, start=0):
    return range(int(start), int(val))


@register.filter('sub')
def subtract(value, arg):
    return value - arg


@register.filter('missing_objects_count')
def missing_objects_count(page):
    return page.paginator.per_page - len(page.object_list)
