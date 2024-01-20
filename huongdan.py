from utils import danh_sach_dai, dais
from helper import replace_vietnamese_characters, is_number
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from datetime import date, timedelta
from telegram.constants import ParseMode
import random
import re



async def huongdan (update: Update, context: ContextTypes.DEFAULT_TYPE, so_vong=2):

    output_str ="""Hướng dẫn lệnh

Ví dụ cú pháp:
1, [tron]
   2d 11,22,33,44,55,66 b100 tron (tin nhắn đầy đủ) * trộn ramdom toàn bộ các số lại blo 100 *
 
2, [chia]
   2d 11,22,33,44,55,66 b100 chia 3 (tin nhắn đầy đủ)  chia ra làm 3 cụm số đánh blo 100 11,22,33 blo 100 , lấy theo tứ tự
   
3, [chiatron]
   2d 11,22,33,44,55,66 b100 chiatron 3 (tin nhắn đầy đủ)  vừa chia vừa trộn số lại
 
 
4, [vong2]
   2d 06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong2 (tin nhắn đầy đủ)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong2 (tin nhắn thiếu đài)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong2 (chỉ dãy số)
 
5, [vong3]
   2d 06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong3 (tin nhắn đầy đủ)
   10.12.31.15.16 dx100 vong3
10.12.31 – 10.31.12
10.12.15 10.12.16 10.31.15. 10.31.16 10.15.16
 
6, [vong4]
   2d 06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong4 (tin nhắn đầy đủ)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong4 (tin nhắn thiếu đài)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong4 (chỉ dãy số)
 
7, [vong5]
   2d 06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong5 (tin nhắn đầy đủ)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong5 (tin nhắn thiếu đài)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 dx100 vong5 (chỉ dãy số)
  
 
8, [3con]
   2d 06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 b100 3con (tin nhắn đầy đủ)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 b100 3con (tin nhắn thiếu đài)
   06,36,46,56,76,86,60,61,62,63,64,67,68,32,70 b100 3con (chỉ dãy số)

9, [bo vi:]

00k09 bo vi5

10, [bo hang]

00k30 bo hang2

11, [bo hang bovi]
00k99 bo hang135 bovi246

12, [chiatien]
   2d 06,36,46,56 b100 da50; 2d 42 92 da50 chiatien

13, [phoi]
   2d 06,36,46,56,76,86,60,61,62 b100
   2d 123 789 231 b100 xc100

14, [tach3]

2d 123 789 231 b100 xc100 tach3


"""
    

    await update.message.reply_text(text=output_str,parse_mode =ParseMode.HTML)