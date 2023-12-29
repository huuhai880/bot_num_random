from telegram import Update
from telegram.ext import  ContextTypes
from telegram.constants import ParseMode

from utils import  dais

from helper import replace_vietnamese_characters, is_number

import random
import re


async def handlekeyword_3CON(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_str = replace_vietnamese_characters(update.message.text)

    input_str = input_str.lower()

    #loại bỏ các kí tự đặc biệt
    substrings_to_replace = ["3con","3c","3 con","3 c","3conthang","3ct","3 conthang","3 ct", '/', ';','-',',','\\','.','?','$','&','*','(',')','{','}','[',']']

    input_str = re.sub(r'\s+', ' ', input_str)

    for substring in substrings_to_replace:
        input_str = input_str.replace(substring, ' ')

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
                num_item['kieu']= string

            # nếu là kiểu đánh thì tạo item mới
            
            if index < len(input_str)-1:
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

            number_format = ""

            lst_number = item['so']

            for index_number in range(0, len(lst_number)):

                for i in range(0,10):
                    number_format +=f"{i}{lst_number[index_number]}"

                    # kiểm tra nếu là cuối mảng thì không cộng dấu phẩy

                    if i < 9 and index_number < len(lst_number):
                        number_format +=","

                
                if index_number < len(lst_number)-1:
                    number_format +=","
                        
            
            if item['dai']== '' :
                formatted_str += f"{number_format} {kieu}; "
            else:
                formatted_str += f"{dai} {number_format} {kieu}; "
                        
                    
        output_list.append(formatted_str)

        
    # Join the formatted strings with line breaks
    output_str = '\n'.join(output_list)


    if error_message == True:

        error_message = 'LỖI\n'+output_str

        await update.message.reply_text(text=error_message,parse_mode =ParseMode.HTML)

    else :
        await update.message.reply_text(text=output_str,parse_mode =ParseMode.HTML)
            
    