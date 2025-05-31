import re

def remove_elements_by_pattern(data_list, pattern):
    """
    Removes elements from a list that match a given regular expression pattern.

    Args:
        data_list: The list to filter.
        pattern: The regular expression pattern to match.

    Returns:
        A new list with elements not matching the pattern.
    """
    regex = re.compile(pattern)
    return [item for item in data_list if not regex.search(item)]
