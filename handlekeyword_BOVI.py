from utils import danh_sach_dai, dais
from helper import replace_vietnamese_characters, is_number
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from datetime import date, timedelta
from telegram.constants import ParseMode
import random
import re


pattern_bovi = re.compile(r'k|keo|ke|ko', re.IGNORECASE)

def extract_numbers(input_string):
   
    numbers = [int(num) for num in re.findall(r'\d+', input_string)]
    return numbers

def chuyen_chuoi_sang_so(chuoi, number_skip):
    
    numbers = extract_numbers(chuoi)

    lst_number_skip = list(str(number_skip))
    
    number_array = list(range(numbers[0], numbers[1] + 1))


    filtered_numbers = number_array

    for _number_skip in lst_number_skip:
        filtered_numbers = [num for num in number_array if int(num) % 10 != int(_number_skip)]
   
    formatted_array = ["{:02d}".format(num) for num in filtered_numbers]

    return formatted_array



async def handlekeyword_BOVI (update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("async def handlekeyword_BOVI (update: Update, context: ContextTypes.DEFAULT_TYPE):")

    input_str = replace_vietnamese_characters(update.message.text)

    input_str = input_str.lower()

    substrings_to_replace = [ '/', ';','-',',','\\','.','?','$','&','*','(',')','{','}','[',']']

    input_str = re.sub(r'\s+', ' ', input_str)

    for substring in substrings_to_replace:
        input_str = input_str.replace(substring, ' ')
    

    input_str.replace('keo', 'k')

    input_str.replace('ke', 'k')

    input_str.replace('ko', 'k')

    input_str = re.sub(r'(\d+)(da|b|x|dx|dd+)', r'\1 \2', input_str)

    input_str = re.sub(r'([d])\s+(\d)', r'\1\2', input_str)

    input_str = re.sub(r'([a-zA-z])\s+([a-zA-z])', r'\1\2', input_str)

    input_str = re.sub(r'(\d+)(n+)', r'\1', input_str)
    
    pattern = re.compile(r'(\d[d])')

    input_str = pattern.sub(r'\1 ', input_str)


    # tach lấy số hoán vị

    input_str = re.sub(r'(bo\s*vi|bovi|bv+)(\d+)', r'|\2', input_str)
 
    input_str = input_str.strip()

    #Tách mảng lấy vị trí bỏ vị
    input_str = input_str.split('|')

    if len(input_str) ==2:

        number_skip = input_str[1]

        # tách giá trị theo tin và lệnh
        str_array = input_str[0].split(' ')
        format_array_muns = []
        num_index = -1

        for index, string in enumerate(str_array):

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

            if pattern_bovi.search(replace_vietnamese_characters(string)):

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

                # Format the string and append it to the output list
            formatted_str = ""

            if len(item['so']) == 0 :
                formatted_str += 'Lỗi tin không có dãy số: \n'
                formatted_str += f"<code>{dai} {kieu}</code> \n"
                error_message=True
            
            else:

                for  so in item['so']:

                    output_str_format = chuyen_chuoi_sang_so(so,number_skip)

                    print(output_str_format)

                    if item['dai']== '' :
                        formatted_str += f"{' '.join(output_str_format)} {kieu}; "
                    else:
                        formatted_str += f"{dai} {' '.join(output_str_format)} {kieu}; "
                
            
            output_list.append(formatted_str)

        output_str = '\n'.join(output_list)


        print(output_str)

        if error_message == True:

            error_message = 'LỖI\n'+output_str

            await update.message.reply_text(text=error_message,parse_mode =ParseMode.HTML)

        else :
            await update.message.reply_text(text=output_str,parse_mode =ParseMode.HTML)
    else :
            await update.message.reply_text(text='LỖI\n'+"Bỏ vị có dạng 00k09 bo vi[đơn vị bỏ]",parse_mode =ParseMode.HTML)