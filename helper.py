from utils import vietnamese_to_english_mapping
import re

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


def laDai(index, noi_dung_arr):

    if index < 0 or index >= len(noi_dung_arr):
        return False

    item = noi_dung_arr[index]

    if not any(char.isalpha() for char in item):  # If there are no letters, return False
        return False
    
    if re.match(r"1d|2d|3d|4d|1dai|2dai|3dai|4dai|dc|dp|chinh|chanh|phu", item):  # If it matches the pattern, return True
        return True

    item_arr = item.split(',')
    
    if len(item_arr) > 4:
        return False

    for code in item_arr:
        if re.match(r"1d|2d|3d|4d|1dai|2dai|3dai|4dai", code):
            return False
        
    return False


def LayViTriDaiCuaKieu(index_of_kieu, noi_dung_arr):

    if index_of_kieu < 0 or index_of_kieu >= len(noi_dung_arr):
        return -1  # Invalid index

    vi_tri_dai = index_of_kieu - 1
    while vi_tri_dai >= 0:
        if laDai(vi_tri_dai, noi_dung_arr):
            return vi_tri_dai

        vi_tri_dai -= 1

    return -1

def laSo( index, noi_dung_arr):
        if index < 0 or index >= len(noi_dung_arr):
            return False

        # Check if it is a valid number format
        item = noi_dung_arr[index]
        chi_chua_ky_tu_so = bool(re.match('^[0-9]+$', item))  # Contains only digits
        
        la_so = chi_chua_ky_tu_so 

        # The element to the left of the current position must be a "dai" or an element containing only numbers
        ben_trai_la_dai = laDai(index - 1, noi_dung_arr)
        ben_trai_la_so = bool(re.match('^[0-9]+([,][0-9]+)?$',noi_dung_arr[index - 1]))  # Contains numbers and commas
        ben_trai_hop_le = ben_trai_la_dai or ben_trai_la_so

        return la_so and ben_trai_hop_le

def LaySoCuaKieu(index_of_kieu,noi_dung_arr):
        result = []
        if index_of_kieu < 0 or index_of_kieu >= len(noi_dung_arr):
            return result  # Invalid, return empty list

        i = index_of_kieu - 1
        while i >= 0:
            if laSo(i, noi_dung_arr):
                result.append(noi_dung_arr[i])
            else:
                if len(result) >= 0:
                    return result[::-1]

            i -= 1

        return result[::-1]

def LayViTriDiemCuaKieu(index_of_kieu, noi_dung_arr):
        if index_of_kieu < 1 or index_of_kieu >= len(noi_dung_arr) - 1:
            return -1  # Invalid

        if bool(re.match('^[0-9]+([,][0-9]+)?$', noi_dung_arr[index_of_kieu + 1])):
            return index_of_kieu + 1

        return -1