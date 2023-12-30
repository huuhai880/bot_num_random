from utils import danh_sach_dai, dais
from helper import replace_vietnamese_characters, is_number
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from datetime import date, timedelta
from telegram.constants import ParseMode
import random
import re

from itertools import combinations



def check_element_exit(current_value, array_check, nums_convert):

    element_exists = False

    print(f"array_check: {array_check}")

    if len(nums_convert) > 0:

        status_convert = False               

        for index_convert in range(0, len(nums_convert)):

            print(f"array_check[j]: {current_value}")
            print(f"nums_convert[index_convert]: {nums_convert[index_convert]}")


            common_elements_convert = [value for value in current_value if value in  nums_convert[index_convert]]

            print(f"common_elements_convert: {common_elements_convert}")

            if len(common_elements_convert) > 1:

                status_convert = True

                break
        
        if status_convert == True:

            element_exists = True


    if element_exists == False:

        if len(array_check) > 0:

            for j in range(0, len(array_check)):

                common_elements = [value for value in current_value if value in array_check[j]]

                # nếu có kêt quả trùng thì loại
                if len(common_elements) > 1:
                    
                    element_exists = True

                    break
    
    return element_exists

async def tao_ket_qua(danh_sach, so_vong=2, nums_convert=[]):

    combinations_list = list(combinations(danh_sach,so_vong ))

    combinations_list = [list(pair) for pair in combinations_list]

    seen_combinations = []

    _combinations = combinations_list

    if  len(nums_convert) > 0:

        _combinations = []

        for comb in combinations_list:

            is_valid = True

            for existing_comb in nums_convert:

                common_elements = set (comb) & set(existing_comb)

                if len(common_elements) > 1:
                    is_valid = False
                    break

            if is_valid == True:
               
                _combinations. append(comb)
        

    for comb in _combinations:

        is_valid = True

        for existing_comb in seen_combinations:

            common_elements = set (comb) & set(existing_comb)

            if len(common_elements) > 1:
                is_valid = False
                break

        if is_valid:
           
            seen_combinations. append(comb)


    return seen_combinations


async def handlekeyword_VONG (update: Update, context: ContextTypes.DEFAULT_TYPE, so_vong=2):

    input_str = replace_vietnamese_characters(update.message.text)

    input_str = input_str.lower()

    input_str = re.sub(r'(\d+)([bBx])', r'\1 \2', input_str)

    #loại bỏ các kí tự đặc biệt
    substrings_to_replace = [f'vong {so_vong}',f'vong{so_vong}',f'v{so_vong}',f'v {so_vong}', '/', ';','-',',','\\','.','?','$','&','*','(',')','{','}','[',']']

    input_str = re.sub(r'\s+', ' ', input_str)

    for substring in substrings_to_replace:
        input_str = input_str.replace(substring, ' ')

    input_str = re.sub(r'([a-zA-Z])\s+(\d)', r'\1\2', input_str)

    pattern = re.compile(r'(\d[a-zA-Z])')

    # Use the sub function to insert a space after the first character in each matched sequence
    input_str = pattern.sub(r'\1 ', input_str)

    input_str = input_str.strip()


    input_str = input_str.split(' ')
    
    input_str = list(filter(lambda x: x != "", input_str))

    format_array_muns = []  

    num_index = -1

    for index, string in enumerate(input_str):

        string = string.strip()
        
        #kiểm tra xem ký tự đó có phải là đài hay không
        if string in dais:
            
            if len(format_array_muns) >0 and len(format_array_muns)-1 == num_index and format_array_muns[num_index]['dai'] =='' :
                
                num_item = format_array_muns[num_index]
                num_item['dai']= string

            else :

                num_item = {}
                num_item['dai']= string
                num_item['so']= []
                num_item['kieu']= ''
                format_array_muns.append(num_item)
                num_index += 1

        if is_number(string):

            if len(format_array_muns) > 0 :
                    
                num_item = format_array_muns[num_index]
                num_item['so'].append(string)

            else :

                num_item = {}
                num_item['dai']= ''
                num_item['so']= [string]
                num_item['kieu']= ''
                format_array_muns.append(num_item)
                num_index += 1
        
        if string not in dais and string.startswith(('b','x','d','bl','dx','xd')) :

            if len(format_array_muns) > 0 :

                num_item = format_array_muns[num_index]
                num_item['kieu'] += string
                num_item['kieu'] += " "

            # nếu là kiểu đánh và item phía sau cũng là kiểu đánh thì không tạo mới
            
            if index < len(input_str)-1 and (index +1) < len(input_str) and not input_str[index+1].startswith(('b','x','d','bl','dx','xd')) :
                new_num_item = {}
                new_num_item['dai']= ''
                new_num_item['so']= []
                new_num_item['kieu']= ''
                format_array_muns.append(new_num_item)
                num_index += 1
            
                
    # sau khi format số bắt đầu tách từng tin và validate

    output_list = []

    error_message=False

    # print(format_array_muns)

    output_str = ""

    for item in format_array_muns:

        dai = item['dai']

        nums_convert = await tao_ket_qua(random.sample(item['so'], len(item['so'])), so_vong,[])

        
        kieu = item['kieu']

        output_str +=f"[vong {so_vong}: {len(nums_convert)}] \n\n"

        # Format the string and append it to the output list
        formatted_str = ""

        if item['kieu']== '' :
            formatted_str += 'Lỗi tin không kết thúc bằng kiểu: \n'
            formatted_str += f"<code>{dai} {' '.join(item['so'])}</code>\n"
            error_message=True
        
        elif len(item['so']) == 0 :
            formatted_str += 'Lỗi tin không có dãy số: \n'
            formatted_str += f"<code>{dai} {kieu}</code> \n"
            error_message=True
        
        else:

            for item_num in nums_convert:
                    
                    so = ','.join(item_num)

                    if item['dai']== '' :

                        formatted_str += f"{so} {kieu}; "
                    else:

                        formatted_str += f"{dai} {so} {kieu}; "
                    


        output_list.append(formatted_str)

        
        # Join the formatted strings with line breaks
        output_str += '; '.join(output_list)


        #kiểm tra xem đã đủ các cặp số hay chưa

        total_cap_so = int(len(item['so']) * (len(item['so']) - 1) / 2)


        if len(nums_convert) < total_cap_so and so_vong > 2:
            number_exists= []
            number_exists.extend(nums_convert)

            output_list = []

            for i in range(so_vong - 1, 1 , -1):

                _nums_convert = await tao_ket_qua(random.sample(item['so'], len(item['so'])), i, number_exists)
                
                formatted_str=""

                print(_nums_convert)

                if len(_nums_convert) > 0:

                    for item_num in _nums_convert:

                        if item['dai']== '' :
                            formatted_str += f"{ ','.join(item_num) } {kieu}; "
                        else:
                            formatted_str += f"{dai} {','.join(item_num)} {kieu}; "

                    output_list.append(formatted_str)

                    output_str +=f"\n\n[vong {i}: {len(_nums_convert)}] \n\n"

                    number_exists.extend(_nums_convert)

                output_str += '; '.join(output_list)

    if error_message == True:

        error_message = f'Vòng {so_vong}\nLỖI\n'+output_str

        await update.message.reply_text(text=error_message,parse_mode =ParseMode.HTML)

    else :

        await update.message.reply_text(text=output_str,parse_mode =ParseMode.HTML)

        
        


   