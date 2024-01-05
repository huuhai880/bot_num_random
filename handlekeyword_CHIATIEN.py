from telegram import Update
from telegram.ext import  ContextTypes
from telegram.constants import ParseMode
from utils import  dais
from helper import replace_vietnamese_characters, LayViTriDaiCuaKieu, LaySoCuaKieu, LayViTriDiemCuaKieu
import re
import random

# def divide_money_random_rounded(amount, num_people):
#     # Tạo ngẫu nhiên một danh sách các tỷ lệ phần trăm
#     percentages = [random.uniform(10, 100) for _ in range(num_people)]
#     total_percentage = sum(percentages)

#     # Chuẩn hóa tỷ lệ để tổng là 100%
#     normalized_percentages = [p / total_percentage * 100 for p in percentages]

#     print(normalized_percentages)

#     shares = [round(amount * (p / 100)) for p in normalized_percentages]
#     return shares

def divide_money_random_rounded(amount, num_people):
    # Tạo ngẫu nhiên một danh sách các tỷ lệ phần trăm
    percentages = [random.uniform(10, 100) for _ in range(num_people)]
    total_percentage = sum(percentages)

    # Chuẩn hóa tỷ lệ để tổng là 100%
    normalized_percentages = [p / total_percentage * 100 for p in percentages]

    # Làm cho tỷ lệ phần trăm chia hết cho 5
    # adjusted_percentages = [round(p / 5) * 5 for p in normalized_percentages]

    # print(adjusted_percentages)

    # Tính toán số tiền tương ứng cho mỗi người dựa trên tỷ lệ chuẩn hóa và làm tròn (chia hết cho 5)
    shares = [round(amount * (p / 100) / 5) * 5 for p in normalized_percentages]

    return shares



async def handlekeyword_CHIATIEN(update: Update, context: ContextTypes.DEFAULT_TYPE):

    input_str = replace_vietnamese_characters(update.message.text)

    input_str = input_str.lower()

    input_str = re.sub(r'(\d+)(da|b|x|dx|dd+)', r'\1 \2', input_str)

    input_str = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', input_str)
    input_str = re.sub(r'([a-zA-z])\s+([a-zA-z])', r'\1\2', input_str)

    #loại bỏ các kí tự đặc biệt
    substrings_to_replace = ["chiatien","chia tien","ct","chiat","chia", '/', ';','-',',','\\','.','?','$','&','*','(',')','{','}','[',']']

    input_str = re.sub(r'\s+', ' ', input_str)

    for substring in substrings_to_replace:
        input_str = input_str.replace(substring, ' ')
        

    input_str = input_str.strip()

    input_str = input_str.split(' ')
    
    format_array_muns = []

    for index, string in enumerate(input_str):

        item={}

        string = string.strip()
        
        # lấy kí tự là kiểu
        if string not in dais and string.startswith(('b','x','d','bl','dx','xd','xc')):
            
            #lấy vị trí đài của kiểu
            vi_tri_dai_cua_kieu = LayViTriDaiCuaKieu(index, input_str)

            item["dai"] = ''

            if re.match(r"1d|2d|3d|4d|1dai|2dai|3dai|4dai", input_str[vi_tri_dai_cua_kieu]):
                item["dai"] = input_str[vi_tri_dai_cua_kieu]
            
            print(LaySoCuaKieu(index, input_str))

            item["so"] = LaySoCuaKieu(index, input_str)

            vi_tri_diem_kieu = LayViTriDiemCuaKieu(index,input_str )

            item["kieu"] = input_str[index]

            item["diem"] = input_str[vi_tri_diem_kieu]

            format_array_muns.append(item)

    
    output_list = []

    error_message=False

    print(format_array_muns)

    for item in format_array_muns:

        dai = item['dai']
        random_so = ' '.join(item['so'])
        kieu = item['kieu']
        diem = item['diem']

        # Format the string and append it to the output list
        formatted_str = ""

        num_people = random.randint(2, 5)
        
        result_divide_money = divide_money_random_rounded(int(diem), num_people)

        for _diem in result_divide_money:

            if item['kieu']== '' :

                formatted_str += 'Lỗi tin không kết thúc bằng kiểu: \n'
                formatted_str += f"<code>{dai} {' '.join(item['so'])}</code>\n"
                error_message=True
            
            elif len(item['so']) == 0 :

                formatted_str += 'Lỗi tin không có dãy số: \n'
                formatted_str += f"<code>{dai} {kieu}</code> \n"
                error_message=True
            
            else:

                if item['dai']== '' :

                    formatted_str += f"{random_so} {kieu}{_diem}; "

                else:

                    formatted_str += f"{dai} {random_so} {kieu}{_diem}; "
            
        
        output_list.append(formatted_str)

        
    # Join the formatted strings with line breaks
    output_str = ''.join(output_list)


    if error_message == True:

        error_message = 'LỖI\n'+output_str

        await update.message.reply_text(text=error_message,parse_mode =ParseMode.HTML)

    else :
        await update.message.reply_text(text=output_str,parse_mode =ParseMode.HTML)
            
    