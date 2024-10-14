from django import template


register = template.Library()


@register.filter
def range_filter(value):
    return range(value)



@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return ''
    print(dictionary.get(key, ''))
    if key is not None:
      return dictionary[key]
    return ''

@register.filter
def getfirst(pair):
    return pair[0]
@register.filter
def getsecond(pair):
    return pair[1]