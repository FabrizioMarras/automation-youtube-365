def title_for_ainsytes(char_name, test_name):
    return f"AInsyte - {char_name} - What to {test_name}"  # Case 4

def title_for_intro(test_name):
    return f"AInsyte decodes {test_name}"  # Case 1

def title_for_personality(char_name, test_name):
    return f"AInsyte decodes {char_name} - {test_name}"  # Case 2

def default_title(char_name, test_type, test_name):
    return f"AInsyte decodes {char_name} - {test_type} {test_name}"  # Case 3

def generate_title(char_name, test_type, test_name):
    strategies = [
        (lambda: test_name in ['Watch', 'Follow'], lambda: title_for_ainsytes(char_name, test_name)),
        (lambda: char_name.lower() == 'intro', lambda: title_for_intro(test_name)),
        (lambda: test_type == 'Personality', lambda: title_for_personality(char_name, test_name))
    ]
    
    for condition, strategy in strategies:
        if condition():
            return strategy()
    
    # Default case
    return default_title(char_name, test_type, test_name)