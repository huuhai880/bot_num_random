from utils import vietnamese_to_english_mapping, danh_sach_dai, dais

def replace_vietnamese_characters(input_string):
    
    # Iterate through the characters in the input string and replace if found in the dictionary
    output_string = ''
    for char in input_string:
        if char in vietnamese_to_english_mapping:
            # Use the English equivalent if the character is in the dictionary
            output_string += vietnamese_to_english_mapping[char]
        else:
            # Keep the original character if not found in the dictionary
            output_string += char

    return output_string

def is_number(value):
    return str(value).isdigit()