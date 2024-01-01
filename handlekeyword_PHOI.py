from telegram import Update
from telegram.ext import  ContextTypes
from telegram.constants import ParseMode

from utils import  dais

from helper import replace_vietnamese_characters, is_number

import random
import re


async def handlekeyword_PHOI(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_str = replace_vietnamese_characters(update.message.text)

    input_str = input_str.lower()

    #loại bỏ các kí tự đặc biệt
    substrings_to_replace = ["phoi","p", '/', ';','-',',','\\','.','?','$','&','*','(',')','{','}','[',']']

    input_str = re.sub(r'\s+', ' ', input_str)

    for substring in substrings_to_replace:
        input_str = input_str.replace(substring, ' ')

    input_str = re.sub(r'(\d+)(da|b|x|dx|dd+)', r'\1 \2', input_str)

    input_str = re.sub(r'([d])\s+(\d)', r'\1\2', input_str)
    input_str = re.sub(r'([a-zA-z])\s+([a-zA-z])', r'\1\2', input_str)

    pattern = re.compile(r'(\d[d])')

    # Use the sub function to insert a space after the first character in each matched sequence
    input_str = pattern.sub(r'\1 ', input_str)

    input_str = input_str.strip()


    input_str = input_str.split(' ')
    
    format_array_muns = []

    num_index = -1

    for index, string in enumerate(input_str):

        string = string.strip()
        
        #kiểm tra xem ký tự đó có phải là đài hay không
        if string in dais:
            
            if len(format_array_muns) > 0 and len(format_array_muns)-1 == num_index and format_array_muns[num_index]['dai'] =='' :
                
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
    
    output_list = []

    error_message=False

    for item in format_array_muns:

        dai = item['dai']
        kieu = item['kieu']
        random_number = random.sample(item['so'], len(item['so']))

        int_list = list(map(str, random_number))

        result = []
        # kiểm tra xem nếu list số lớn hơn 3 thì chia đều thành 3
        if len(int_list) == 3 and kieu.startswith(('da','d')):

            result = [int_list[i:i+3] for i in range(0, len(int_list), 3)]
        
        elif len(int_list) == 4 and kieu.startswith(('da','d')):

            result = [int_list[i:i+2] for i in range(0, len(int_list), 2)]


        elif len(int_list) == 3:

            result = [int_list[i:i+2] for i in range(0, len(int_list), 2)]
        
        
        elif len(int_list) > 3:
            # Reshape the list into a 3x3 matrix
            result = [int_list[i:i+3] for i in range(0, len(int_list), 3)]

       
        
        for _number in result:

            # Format the string and append it to the output list
            formatted_str = ""

            # if item['kieu']== '' :
            #     formatted_str += 'Lỗi tin không kết thúc bằng kiểu: \n'
            #     formatted_str += f"<code>{dai} {' '.join(item['so'])}</code>\n"
            #     error_message=True
            
            if len(item['so']) == 0 :
                formatted_str += 'Lỗi tin không có dãy số: \n'
                formatted_str += f"<code>{dai} {kieu}</code> \n"
                error_message=True

            elif kieu.startswith(('da','d')) and len(_number) == 1:

                formatted_str += 'Lỗi kiểu đá tối thiểu phải có 2 số: \n'
                formatted_str += f"<code>{dai} {' '.join(item['so'])} {kieu}</code> \n"
                error_message=True

            else:

                lst_number = "-".join(map(str, _number))

                if item['dai']== '' :
                    formatted_str += f"{lst_number} {kieu}; "
                else:
                    formatted_str += f"{dai} {lst_number} {kieu}; "
                        
                    
            output_list.append(formatted_str)

    
    # Join the formatted strings with line breaks
    output_str = ' '.join(output_list)

    if error_message == True:

        error_message = 'LỖI\n'+output_str

        await update.message.reply_text(text=error_message,parse_mode =ParseMode.HTML)

    else :
        await update.message.reply_text(text=output_str,parse_mode =ParseMode.HTML)
            
    