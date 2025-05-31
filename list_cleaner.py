def extract_label_and_grouped_numbers(data):
    result = []

    # Separate label and first number pair
    first = data[0]
    parts = first.rsplit(' ', 2)
    label = ' '.join(parts[:-2])
    number = ' '.join(parts[-2:])
    result.append(label)
    result.append(number)

    for item in data[1:]:
        if ',' in item and ' ' in item:
            # Handle the special case like "9,7 4 051"
            comma_part, rest = item.split(' ', 1)
            result.append(comma_part)
            result.append(rest)
        elif ' ' in item and not any(c.isalpha() for c in item):
            # Handle regular numeric pairs like "3 278"
            result.append(item)
        else:
            # Already fine (e.g., "12,0" or "14,9")
            result.append(item)

    return result
