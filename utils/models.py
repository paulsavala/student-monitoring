

def add_to_list(orig_list, items):
    if not isinstance(items, list):
        items = [items]
    if orig_list is None:
        orig_list = []
    orig_list += items
    return orig_list


def remove_from_list(orig_list, items, ignore_warnings=False):
    if not isinstance(items, list):
        items = [items]
    for item in items:
        if not ignore_warnings:
            assert item in orig_list, f'{item} is not in list'
        orig_list.remove(item)
    return orig_list
