from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from telegram.constants import ParseMode

from helper import replace_vietnamese_characters, is_number

from handlekeyword_CHIA import handlekeyword_CHIA
from handlekeyword_CHIATRON import handlekeyword_CHIATRON
from handlekeyword_VONG import handlekeyword_VONG
from handlekeyword_TRON import handlekeyword_TRON
from handlekeyword_3CON import handlekeyword_3CON
from handlekeyword_PHOI import handlekeyword_PHOI
from handlekeyword_CHIATIEN import handlekeyword_CHIATIEN

# Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
TOKEN = '6808395010:AAGvk6Wgg3eqm-nj12N6loWWn4lcDJMLZNY'


# Example usage

async def handlerListenMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message_text = update.message.text

    if "chiatron" in replace_vietnamese_characters(message_text).lower():

        print("chiatron")
        # Perform some action here for the 'chia' case
        await handlekeyword_CHIATRON(update, context)

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
        
        print("vong4")
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
    
    else:
        
        await update.message.reply_text(text="Lỗi không có từ khoá hành động",parse_mode =ParseMode.HTML)

        # Perform some default action if needed

def main():

    app = Application.builder().token(TOKEN).build()

    # command

    # app.add_handler(MessageHandler(filters.ChatType.GROUP & filters.TEXT, handlerListenMessage))

    app.add_handler(MessageHandler(filters.TEXT, handlerListenMessage))

    app.run_polling(poll_interval=1)


if __name__ == '__main__':
    main()  
