def remove_duplicate_lists(list_of_lists):
    """Removes duplicate lists from a list of lists, preserving order.

    Args:
        list_of_lists: A list of lists.

    Returns:
        A new list of lists with duplicates removed.
    """
    unique_lists = []
    seen = set()  # Use a set to keep track of seen lists (as tuples)

    for sublist in list_of_lists:
        # Convert the sublist to a tuple because lists are not hashable
        sublist_tuple = tuple(sublist)
        if sublist_tuple not in seen:
            seen.add(sublist_tuple)
            unique_lists.append(sublist)
    return unique_lists


def remove_empty_lists(list_of_lists):
    return [sublist for sublist in list_of_lists if sublist]

def remove_problem_lists(list_of_lists):
    return [sublist for sublist in list_of_lists if not len(sublist) == 1]
