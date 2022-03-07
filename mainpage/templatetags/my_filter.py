from django import template

register = template.Library()


@register.filter(name='done')
def done(value):
    return value.filter(done=True)


@register.filter(name='not_done')
def done(value):
    return value.filter(done=False)
