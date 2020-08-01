

def add_to_list(orig_list, items, allow_duplicates=False, unique_attr=None):
    if not isinstance(items, list):
        items = [items]
    if orig_list is None:
        orig_list = []
    if not isinstance(orig_list, list):
        orig_list = [orig_list]
    orig_list += items
    return orig_list


def remove_from_list(orig_list, items, allow_duplicates=False, unique_attr=None, ignore_warnings=False):
    if not isinstance(items, list):
        items = [items]
    if not isinstance(orig_list, list):
        orig_list = [orig_list]
    if unique_attr is not None:
        orig_list_identifiers = {getattr(x, unique_attr): x for x in orig_list}
        items_identifiers = {getattr(x, unique_attr): x for x in items}
    else:
        orig_list_identifiers = {x: x for x in orig_list}
        items_identifiers = {x: x for x in items}

    for item_identifier in items_identifiers:
        if not ignore_warnings:
            assert item_identifier in orig_list_identifiers, f'{item_identifier} is not in list'
        while item_identifier in orig_list_identifiers:
            del orig_list_identifiers[item_identifier]

    return [orig_list_identifiers[x] for x in orig_list_identifiers]
