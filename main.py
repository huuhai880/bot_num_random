from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CommandHandler

from telegram.constants import ParseMode
import re
from helper import replace_vietnamese_characters, is_number

from handlekeyword_CHIA import handlekeyword_CHIA
from handlekeyword_CHIATRON import handlekeyword_CHIATRON
from handlekeyword_VONG import handlekeyword_VONG
from handlekeyword_TRON import handlekeyword_TRON
from handlekeyword_3CON import handlekeyword_3CON
from handlekeyword_PHOI import handlekeyword_PHOI
from handlekeyword_CHIATIEN import handlekeyword_CHIATIEN
from handlekeyword_BOVI import handlekeyword_BOVI
from handlekeyword_BOHANG import handlekeyword_BOHANG
from handlekeyword_BOHANGVABOVI import handlekeyword_BOHANGVABOVI
from handlekeyword_TACH3 import handlekeyword_TACH3
from huongdan import huongdan

# Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
TOKEN = '6178433211:AAGekPQz_lY_4Sex-3T5n-fiy41n4GSmVe8'

pattern_bovi = re.compile(r'bo\s*vi|bovi|bv|vi', re.IGNORECASE)

pattern_bohang = re.compile(r'bo\s*hang|bohang|bh|hang', re.IGNORECASE)
# Example usage

async def handlerListenMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.message.text

    if "chiatron" in replace_vietnamese_characters(message_text).lower():

        print("chiatron")
        # Perform some action here for the 'chia' case
        await handlekeyword_CHIATRON(update, context)

    elif pattern_bovi.search(replace_vietnamese_characters(message_text)) and pattern_bohang.search(replace_vietnamese_characters(message_text)):
        print("bo_vi and bo_hang")
        # Perform some action here for the 'chia' case
        await handlekeyword_BOHANGVABOVI(update, context)

    elif pattern_bovi.search(replace_vietnamese_characters(message_text)):
        print("bo_vi")
        # Perform some action here for the 'chia' case
        await handlekeyword_BOVI(update, context)
    
    elif pattern_bohang.search(replace_vietnamese_characters(message_text)):
        print("bo_hang")
        # Perform some action here for the 'chia' case
        await handlekeyword_BOHANG(update, context)

    elif replace_vietnamese_characters(message_text).lower().endswith(("3con","3c","3 con","3 c","3conthang","3ct","3 conthang","3 ct")):

        print("3con")
        # Perform some action here for the 'cashe' case
        await handlekeyword_3CON(update, context)
    
    elif replace_vietnamese_characters(message_text).lower().endswith(("phoi","p")):

        print("phoi")
        # Perform some action here for the 'cashe' case
        await handlekeyword_PHOI(update, context)

    elif replace_vietnamese_characters(message_text).lower().endswith(("tron")):

        print("tron")
        # Perform some action here for the 'cashe' case
        await handlekeyword_TRON(update, context)
    
    elif replace_vietnamese_characters(message_text).lower().endswith(("chiatien","chia tien","ct","chiat","chia")):
        print("chiatien")
        # Perform some action here for the 'chia' case
        await handlekeyword_CHIATIEN(update, context)

    elif "chia" in replace_vietnamese_characters(message_text).lower():
        
        print("chia")
        # Perform some action here for the 'chia' case
        await handlekeyword_CHIA(update, context)
    
    elif replace_vietnamese_characters(message_text).lower().endswith(("vong2","vong 2","v 2","v2")):
        
        print("vong2")
        # Perform some action here for the 'chia' case
        await handlekeyword_VONG(update, context, 2)
    
    elif replace_vietnamese_characters(message_text).lower().endswith(("vong3", "vong 3","v 3","v3")):
        
        print("vong3")
        # Perform some action here for the 'chia' case
        await handlekeyword_VONG(update, context, 3)
    
    elif replace_vietnamese_characters(message_text).lower().endswith(("vong4","vong 4","v 4","v4")):
        print("vong4")
        # Perform some action here for the 'chia' case
        await handlekeyword_VONG(update, context, 4)
    
    elif replace_vietnamese_characters(message_text).lower().endswith(("vong5","vong 5","v 5","v5")):
        print("vong5")
        # Perform some action here for the 'chia' case
        await handlekeyword_VONG(update, context, 5)
    
    elif replace_vietnamese_characters(message_text).lower().endswith(("tach3","tach 3","t3","t 3")):
        print("tach 3")
        # Perform some action here for the 'chia' case
        await handlekeyword_TACH3(update, context)
    
    else:
        
        await update.message.reply_text(text="Lỗi không có từ khoá hành động",parse_mode =ParseMode.HTML)

        # Perform some default action if needed

def main():

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("huongdan", huongdan))
    # command

    # app.add_handler(MessageHandler(filters.ChatType.GROUP & filters.TEXT, handlerListenMessage))

    app.add_handler(MessageHandler(filters.TEXT, handlerListenMessage))

    



    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()  
