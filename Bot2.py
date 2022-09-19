#!/usr/bin/python3
from argparse import Namespace
from csv import register_dialect
from dataclasses import replace
from email.message import Message
from unittest import result
import telebot
import pyodbc
import datetime
from telebot import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

user_dict={}

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=APCKRMPTMD01TV,41433;DATABASE=Namlos;UID=Namlos_user;PWD=Namlos@123')
cursor = conn.cursor()

api = '5572350212:AAFg9UsMwyqiGRD5TmbScUVmBw6BZGi79DQ'
bot = telebot.TeleBot(api)

class User:
  def __init__(self, Nama):
    Nama = None
    Nest = None
    Nest2 = None

def log(message,perintah):
  tanggal = datetime.datetime.now()
  tanggal = tanggal.strftime('%d-%B-%Y')
  nama_awal = message.chat.first_name
  nama_akhir = message.chat.last_name
  id_user = message.chat.id
  text_log = '{}, {}, {} {}, {} \n'.format(tanggal, id_user, nama_awal, nama_akhir, perintah)
  log_bot = open('log_bot.txt','a')
  log_bot.write(text_log)
  log_bot.close()

def ex_id(id):
  result = False
  file=open("log_bot.txt", 'r')
  for line in file:
    if line.strip()==id:
      result = True
  file.close()
  return result


@bot.message_handler(commands=['start'])
def action_start(message):
  log(message,'Start')
  first_name = message.chat.first_name
  last_name = message.chat.last_name
  
  if message.chat.type == "private":
    idk = message.chat.id
    f = open('log_bot.txt','a')
    if(not ex_id(str(idk))):
      f.write("{}\n".format(idk))
      f.close()
      bot.send_message(message.chat.id, 'Hallo, {} {}, perkenalkan saya ares yang akan membantumu mencari Nest Toy ☺️'.format(first_name,last_name))
      bot.send_message(message.chat.id, "Sebelum kita mulai tolong registrasi terlebih dahulu ya 😉")
      #buat custom keyboard
      a = types.KeyboardButton('Register ✅')
      custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(a)

      bot.send_message(message.chat.id,'Register sekarang?', reply_markup=custom)

    else:
      bot.send_message(message.chat.id, text="*Hi {} {}, Selamat datang kembali 🙋‍♀️*".format(message.chat.first_name,message.chat.last_name),parse_mode="Markdown")
      custom = types.ReplyKeyboardRemove()
      c = types.KeyboardButton('Ambil Nest 📤')
      d = types.KeyboardButton('Kembalikan Nest 📥')
      custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
      bot.send_message(message.chat.id,'Apa yang bisa aku bantu? 😉', reply_markup=custom)


@bot.message_handler(commands=['help'])
def action_help(message: types.Message):
  log(message,'Help')
  first_name = message.chat.first_name
  last_name = message.chat.last_name
  bot.send_message(message.chat.id, '''
Hi {} {}, ini list command yaa
/start --> Memulai Proses Pencarian
/datanest --> Menampilkan Nest yang tersedia
/mynest --> Menampilkan Nest yang di pinjam
/ambil --> Proses Pengambilan Nest
/kembali --> Proses Pengembalian Nest
/akun --> Cek Akun Pengguna
/help --> Melihat Daftar Perintah
'''.format(first_name,last_name))

@bot.message_handler(commands=['kembali'])
def datakembali (message):
  try:
    cursor.execute("select Nest from Nest_Toy where Peminjam_Terakhir='{} {}'".format(message.chat.first_name,message.chat.last_name))
    hasil_sql = cursor.fetchall()

    c = types.KeyboardButton('Cancel')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c)
    for x in hasil_sql:
      markup.add(types.KeyboardButton(str(x).replace(","," ").replace("'","").replace(")","").replace("(","")))
    msg = bot.send_message(message.chat.id,"Pilih Nest yang ingin di kembalikan", reply_markup=markup)
    bot.register_next_step_handler(msg, KembaliNest)

  except Exception as e:
    bot.send_message(message.chat.id, "Belum ada nest yang di pinjam")
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apakah Ada Hal Lain Yang Bisa Ku bantu?', reply_markup=custom)

@bot.message_handler(commands=['ambil'])
def ambil(message):
  d = types.KeyboardButton('Semua Data Nest')
  c = types.KeyboardButton('Cancel')
  
  
  custom = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(d,c)

  bot.send_message(message.chat.id,text="_Tolong lengkapi data berikut!_", reply_markup=custom, parse_mode="Markdown")
  msg=bot.send_message(message.chat.id,text="*Nama Nest Yang ingin di ambil?*", parse_mode="Markdown")
  bot.register_next_step_handler(msg, step4)

@bot.message_handler(commands=['mynest'])
def mynest(message):
  try:
    first_name = message.chat.first_name
    last_name = message.chat.last_name
    bot.send_message(message.chat.id,"Menampilkan data Nest yang dipinjam")
    cursor.execute("select Nest from Nest_Toy where Peminjam_Terakhir='{} {}'".format(first_name,last_name))
    hasil_sql = cursor.fetchall()
    pesan_balasan = ''
    for x in hasil_sql:
        pesan_balasan = pesan_balasan + str(x) + '\n'

    pesan_balasan = pesan_balasan.replace("'", "")
    pesan_balasan = pesan_balasan.replace("(", "")
    pesan_balasan = pesan_balasan.replace(")", "")
    pesan_balasan = pesan_balasan.replace("'", "")

    bot.send_message(message.chat.id, pesan_balasan)

    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apakah Ada Hal Lain Yang Bisa Ku bantu?', reply_markup=custom)

  except Exception as e:
    bot.send_message(message.chat.id, "Belum ada nest yang di pinjam")
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apakah Ada Hal Lain Yang Bisa Ku bantu?', reply_markup=custom)


@bot.message_handler(commands=['akun'])
def action_id(message):
  log(message,'Cek ID')
  first_name = message.chat.first_name
  last_name = message.chat.last_name
  id_telegram = message.chat.id
  
  cursor.execute("select Nama from Register_Nest where ID={}".format(message.chat.id))
  hasil_sql = cursor.fetchone()
  cursor.execute("select KPK from Register_Nest where ID={}".format(message.chat.id))
  hasil_sql1 = cursor.fetchone()


  bot.send_message(message.chat.id, '''
Hallo, ini Detail Akun kamu
UserNama Telegram = {} {}
ID Telegram= {}
Nama = {}
KPK = {}
'''.format(first_name,last_name, id_telegram,hasil_sql,hasil_sql1).replace(","," ").replace("'","").replace(")","").replace("(",""))

@bot.message_handler(regexp='Register')
def kb_answer(message):
    c = types.KeyboardButton('cancel')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c)

    msg = bot.send_message(message.chat.id, 'Oke, Beritahu aku siapa namamu?', reply_markup=custom)
    bot.register_next_step_handler(msg, step1)

@bot.message_handler(regexp='Sudah Register')
def kb_answer1(message):
    custom = types.ReplyKeyboardRemove()
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apa yang bisa aku bantu? 😉', reply_markup=custom)


def step1(message):
  try:
    id_user = message.chat.id
    Nama = message.text
    if Nama == 'cancel':
        custom = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,text="*Prosess di batalkan!!*", reply_markup=custom, parse_mode="Markdown")
        a = types.KeyboardButton('Register ✅')

        custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(a)

        bot.send_message(message.chat.id,'Register sekarang?', reply_markup=custom)
    else:
      User.Nama = Nama
      user_dict[message.chat.id]= User.Nama

      c = types.KeyboardButton('cancel')
      custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c)
      msg=bot.send_message(message.chat.id, 'Hi ' + Nama + ' Nama yang bagus, Beritahu aku KPK mu?', reply_markup=custom)
   
      bot.register_next_step_handler(msg,  step2)
  except Exception as e:
    bot.send_message(message.chat.id, 'Kesalahan name step')

def step2(message):
  id_user = message.chat.id
  texts = message.text
  if texts == 'cancel':
    custom = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,text="*Prosess di batalkan!!*", reply_markup=custom, parse_mode="Markdown")
    a = types.KeyboardButton('Register ✅')

    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(a)

    bot.send_message(message.chat.id,'Register sekarang?', reply_markup=custom)
  else:
    KPK = texts
    if not KPK.isdigit():
      msg = bot.send_message(message.chat.id, text="_KPK haruslah sebuah angka. Berapakah KPK anda?_", parse_mode="Markdown")
      bot.register_next_step_handler(msg, step2)
      return
    texts = message.text
    KPK = texts
 
    insert = 'INSERT INTO Register_Nest (Nama, KPK, ID, Username) VALUES (?,?,?,?)'
    val = (User.Nama, KPK ,id_user, message.chat.first_name)
    cursor.execute(insert, val)
    conn.commit()
    bot.send_message(message.chat.id, 'Terima Kasih, Data berhasil diinput')
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    msg = bot.send_message(message.chat.id,'Apa yang bisa aku bantu? 😉', reply_markup=custom)


@bot.message_handler(regexp='Batalkan')
def batal(message):
  custom = types.ReplyKeyboardRemove()
  bot.send_message(message.chat.id,text="*Prosess di batalkan!!*", reply_markup=custom, parse_mode="Markdown")
  c = types.KeyboardButton('Ambil Nest 📤')
  d = types.KeyboardButton('Kembalikan Nest 📥')
  custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
  bot.send_message(message.chat.id,'Apa yang bisa aku bantu? 😉', reply_markup=custom)


@bot.message_handler(regexp='Ambil Nest')
def step(message):
  d = types.KeyboardButton('Semua Data Nest')
  c = types.KeyboardButton('Cancel')
  
  
  custom = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True).add(d,c)

  bot.send_message(message.chat.id,text="_Tolong lengkapi data berikut!_", reply_markup=custom, parse_mode="Markdown")
  msg=bot.send_message(message.chat.id,text="*Nama Nest Yang ingin di ambil?*", parse_mode="Markdown")
  bot.register_next_step_handler(msg, step4)




@bot.message_handler(regexp='Kembalikan Nest')
def step3(message):
  try:
    cursor.execute("select Nest from Nest_Toy where Peminjam_Terakhir='{} {}'".format(message.chat.first_name,message.chat.last_name))
    hasil_sql = cursor.fetchall()

    c = types.KeyboardButton('Cancel')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c)
    for x in hasil_sql:
      markup.add(types.KeyboardButton(str(x).replace(","," ").replace("'","").replace(")","").replace("(","")))
    msg = bot.send_message(message.chat.id,"Pilih Nest yang ingin di kembalikan", reply_markup=markup)
    bot.register_next_step_handler(msg, KembaliNest)

  except Exception as e:
    bot.send_message(message.chat.id, "Belum ada nest yang di pinjam")
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apakah Ada Hal Lain Yang Bisa Ku bantu?', reply_markup=custom)
    

def step4(message):
  try:
    id_user = message.chat.id
    Nest = message.text
    if Nest == 'Cancel':
        custom = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,text="*Prosess di batalkan!!*", reply_markup=custom, parse_mode="Markdown")
        c = types.KeyboardButton('Ambil Nest 📤')
        d = types.KeyboardButton('Kembalikan Nest 📥')
        custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
        bot.send_message(message.chat.id,'Apa yang bisa aku bantu? 😉', reply_markup=custom)
    elif Nest == 'Semua Data Nest':
      id_user = message.chat.id
      bot.send_message(message.chat.id,"Menampilkan data Nest")
      bot.send_document(message.chat.id, open('Data.csv','rb'))
      msg=bot.send_message(message.chat.id,text="*Nama Nest Yang ingin di ambil?*", parse_mode="Markdown")
      bot.register_next_step_handler(msg, step4)

    else:
      User.Nest = Nest
      bot.send_message(message.chat.id, 'Kamu akan meminjam Nest ' + User.Nest + ' Berikut Datanya')
      cursor.execute("select Nest, Lokasi, Peminjam_Terakhir, Status from Nest_Toy where Nest='{}'".format(User.Nest))
      hasil_sql = cursor.fetchall()
      pesan_balasan = ''
      for x in hasil_sql:
         pesan_balasan = "Nama Nest : " + x[0] + '\n' +"Lokasi: " + x[1] + '\n' +"Peminjam : " + x[2] + '\n' +"Status : " + x[3] + '\n'
  
      pesan_balasan = pesan_balasan.replace("'","")
  
  #menghilangkan tanda kurung
      pesan_balasan = pesan_balasan.replace("(","")
      pesan_balasan = pesan_balasan.replace(")","")
  #menghilangkan tanda koma
      pesan_balasan = pesan_balasan.replace(","," ")
    
      bot.send_message(message.chat.id, pesan_balasan)

      if x[3] == 'Dipinjam':
        bot.send_message(message.chat.id, text="*Sepertinya nest yang kamu pilih sedang digunakan!!*", parse_mode="Markdown")
        msg = bot.send_message(message.chat.id,'Coba Nest Lain? 😉')
        bot.register_next_step_handler(msg, step4)

      else:
        msg=bot.send_message(message.chat.id,text="_Beritahu aku lokasi Pemindahan Nest?_", parse_mode="Markdown")
        bot.register_next_step_handler(msg, Ambil)


  except Exception as e:
    bot.reply_to(message, "Nest Tidak terdaftar!")
    msg = bot.send_message(message.chat.id,'Coba Nest Lain? 😉')
    bot.register_next_step_handler(msg, step4)

def Ambil(message):
    id_user = message.chat.id
    Lokasi = message.text
    Status = "Dipinjam"
    
    cursor.execute("UPDATE Nest_Toy SET Lokasi='{}', Peminjam_Terakhir='{} {}', Status='{}' WHERE Nest='{}'".format(Lokasi, message.chat.first_name,message.chat.last_name, Status, User.Nest))
    conn.commit()
    bot.send_message(message.chat.id, 'Terima Kasih, Data berhasil diinput')
    
    cursor.execute("select Nest, Lokasi, Peminjam_Terakhir, Status from Nest_Toy where Nest='{}'".format(User.Nest))
    hasil_sql = cursor.fetchall()
    pesan_balasan = ''
    for x in hasil_sql:
      pesan_balasan = "Nama Nest : " + x[0] + '\n' +"Lokasi: " + x[1] + '\n' +"Peminjam : " + x[2] + '\n' +"Status : " + x[3] + '\n'
  
  
      pesan_balasan = pesan_balasan.replace("'","")
  
  #menghilangkan tanda kurung
      pesan_balasan = pesan_balasan.replace("(","")
      pesan_balasan = pesan_balasan.replace(")","")
  #menghilangkan tanda koma
      pesan_balasan = pesan_balasan.replace(",","")
    
      bot.send_message(message.chat.id,'Detail update data!' + pesan_balasan)
    
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apakah Ada Hal Lain Yang Bisa Ku bantu?', reply_markup=custom)

def KembaliNest(message):
  try:
    id_user = message.chat.id
    Nest = message.text
    if Nest == 'Cancel':
        custom = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,text="*Prosess di batalkan!!*", reply_markup=custom, parse_mode="Markdown")
        c = types.KeyboardButton('Ambil Nest 📤')
        d = types.KeyboardButton('Kembalikan Nest 📥')
        custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
        bot.send_message(message.chat.id,'Apa yang bisa aku bantu? 😉', reply_markup=custom)
    else:
      User.Nest = Nest
      bot.send_message(message.chat.id, 'Kamu akan mengembalikan Nest ' + User.Nest + ' Berikut Datanya')
      cursor.execute("select Nest, Lokasi, Peminjam_Terakhir, Status from Nest_Toy where Nest='{}'".format(User.Nest))
      hasil_sql = cursor.fetchall()
      pesan_balasan = ''
      for x in hasil_sql:
        pesan_balasan = "Nama Nest : " + x[0] + '\n' +"Lokasi: " + x[1] + '\n' +"Peminjam : " + x[2] + '\n' +"Status : " + x[3] + '\n'
  
      pesan_balasan = pesan_balasan.replace("'","")
  
      #menghilangkan tanda kurung
      pesan_balasan = pesan_balasan.replace("("," ")
      pesan_balasan = pesan_balasan.replace(")","")
      #menghilangkan tanda koma
      pesan_balasan = pesan_balasan.replace(","," ")
    
      bot.send_message(message.chat.id, pesan_balasan)

      if x[3] == 'Tersedia':
        bot.send_message(message.chat.id, text="*Kamu belum meminjam Nest!!*", parse_mode="Markdown")
        msg = bot.send_message(message.chat.id,'Coba Nest Lain? 😉')
        bot.register_next_step_handler(msg, KembaliNest)
      else:
        c = types.KeyboardButton('Cancel')
  
        custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c)
  
        msg=bot.send_message(message.chat.id,text="_Beritahu aku lokasi Pengembalian Nest?_",reply_markup=custom, parse_mode="Markdown")
        bot.register_next_step_handler(msg, kembali)
  except Exception as e:
    bot.send_message(message.chat.id, text="*Nest Tidak Terdaftar/ Kamu belum meminjam Nest!!*",parse_mode="Markdown")
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apakah Ada Hal Lain Yang Bisa Ku bantu?', reply_markup=custom)
  

def kembali(message):
  id_user = message.chat.id
  Lokasi = message.text

  if Lokasi == 'Cancel':
    custom = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id,text="*Prosess di batalkan!!*", reply_markup=custom, parse_mode="Markdown")
    c = types.KeyboardButton('Ambil Nest 📤')
    d = types.KeyboardButton('Kembalikan Nest 📥')
    custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
    bot.send_message(message.chat.id,'Apa yang bisa aku bantu? 😉', reply_markup=custom)
  else:
    Status = "Tersedia"
    Peminjam = "-- "


    cursor.execute("UPDATE Nest_Toy SET Lokasi='{}', Peminjam_Terakhir='{}', Status='{}' WHERE Nest='{}'".format(Lokasi,Peminjam , Status, User.Nest))
    conn.commit()
    bot.send_message(message.chat.id, 'Terima Kasih, Data berhasil diupdate!!')

    cursor.execute("select Nest, Lokasi, Peminjam_Terakhir, Status from Nest_Toy where Nest='{}'".format(User.Nest))
    hasil_sql = cursor.fetchall()
    pesan_balasan = ''
    for x in hasil_sql:
      pesan_balasan = "Nama Nest : " + x[0] + '\n' +"Lokasi: " + x[1] + '\n' +"Peminjam : " + x[2] + '\n' +"Status : " + x[3] + '\n'
  
  
      pesan_balasan = pesan_balasan.replace("'","")
  
  #menghilangkan tanda kurung
      pesan_balasan = pesan_balasan.replace("(","|Detail Nest : ")
      pesan_balasan = pesan_balasan.replace(")","")
  #menghilangkan tanda koma
      pesan_balasan = pesan_balasan.replace(","," | ")
    
      bot.send_message(message.chat.id,'Detail update data!' + pesan_balasan)
    
      c = types.KeyboardButton('Ambil Nest 📤')
      d = types.KeyboardButton('Kembalikan Nest 📥')
      custom = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(c,d)
      bot.send_message(message.chat.id,'Apakah Ada Hal Lain Yang Bisa Ku bantu?', reply_markup=custom)


  

print('bot start running')
bot.polling()