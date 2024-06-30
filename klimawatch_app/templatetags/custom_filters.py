from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    # print(f"Getting item with key {key} from dictionary {dictionary}")
    return dictionary.get(key)
