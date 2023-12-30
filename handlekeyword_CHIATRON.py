from utils import danh_sach_dai, dais
from helper import replace_vietnamese_characters, is_number
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
import random
import re


async def chia_dau_so(danh_sach, kich_thuoc):
    # Chia dãy số thành các phần tử con có kích thước cho trước
    phan_tu_con = [danh_sach[i:i+kich_thuoc] for i in range(0, len(danh_sach), kich_thuoc)]

    return phan_tu_con



async def handlekeyword_CHIATRON (update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_str = replace_vietnamese_characters(update.message.text)

    input_str = input_str.lower()

    #loại bỏ các kí tự đặc biệt
    substrings_to_replace = ['chiatron', '/', ';','-',',','\\','.','?','$','&','*','(',')','{','}','[',']']

    input_str = re.sub(r'\s+', ' ', input_str)

    for substring in substrings_to_replace:
        input_str = input_str.replace(substring, ' ')

    input_str = re.sub(r'(\d+)(da|b|x|dx|dd+)', r'\1 \2', input_str)

    input_str = re.sub(r'([d])\s+(\d)', r'\1\2', input_str)

    pattern = re.compile(r'(\d[d])')

    # Use the sub function to insert a space after the first character in each matched sequence
    input_str = pattern.sub(r'\1 ', input_str)

    input_str = input_str.strip()



    if input_str.startswith((danh_sach_dai)):

        input_str = input_str.split(' ')
        
        input_str = list(filter(lambda x: x != "", input_str))

        so_cum = input_str[len(input_str)-1]

        #Kiểm tra xem kí tự cuối của tin có phải là số hay không
        if is_number(input_str[len(input_str)-1]):
            
            # sau khi kiểm tra xoá kí tự cuối 
            input_str = input_str[:-1]

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

            for item in format_array_muns:

                dai = item['dai']
                
                kieu = item['kieu']

                nums_convert = await chia_dau_so(item['so'],int(so_cum))

                formatted_str = ""

                if item['dai']== '' :
                    
                    formatted_str += 'Lỗi tin không bắt đầu bằng tên đài: \n'
                    formatted_str += f"<code>{' '.join(item['so'])} {kieu}</code> \n"
                    error_message=True

                elif item['kieu']== '' :

                    formatted_str += 'Lỗi tin không kết thúc bằng kiểu: \n'
                    formatted_str += f"<code>{dai} {' '.join(item['so'])}</code>\n"
                    error_message=True
                
                elif len(item['so']) == 0 :

                    formatted_str += 'Lỗi tin không có dãy số: \n'
                    formatted_str += f"<code>{dai} {kieu}</code> \n"
                    error_message=True
                    
                else:

                    for item_num in nums_convert:
                        so = ' '.join(item_num)
                        if len(item_num) < int(so_cum):
                            formatted_str += f'Lỗi tin không đủ chia cụm {so_cum}: \n'
                            formatted_str += f"<code>{dai} {so} {kieu}</code> \n"
                            error_message=True
                        else:
                            
                           
                            if item['dai']== '' :
                                formatted_str += f"{' '.join(random.sample(item_num, len(item_num)))} {kieu}; "
                            else:
                                formatted_str += f"{dai} {' '.join(random.sample(item_num, len(item_num)))} {kieu}; "

                            

                output_list.append(formatted_str)
                
            # Join the formatted strings with line breaks
            output_str = '\n'.join(output_list)
                        
            if error_message == True:

                error_message = 'LỖI\n'+output_str

                await update.message.reply_text(text=error_message,parse_mode =ParseMode.HTML)

            else :
                await update.message.reply_text(text=output_str,parse_mode =ParseMode.HTML)

        else:
            await update.message.reply_text(text=f'Tin không có số để chia \n <code>{update.message.text}</code>',parse_mode =ParseMode.HTML)
        


   