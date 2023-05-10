import sqlite3
import telebot
import pathlib
from pathlib import Path
from telebot import types
token = ''
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=['text'])
def start(message):
    allwords = message.text
    access = getAccess(message.chat.id)
    if access[0] == '1':
        global topin
        topin = bot.send_message(chat_id=message.chat.id, text='меню администратора', reply_markup=start_menu_amdina()).message_id
    if allwords:
        bot.send_message(message.chat.id, "📚список предметов📚", reply_markup=start_menu())

def start_menu_amdina():
    markup5 = types.InlineKeyboardMarkup()
    markup5.add(types.InlineKeyboardButton("добавление в базу", callback_data="add"))
    markup5.add(types.InlineKeyboardButton("изменение базы", callback_data="add"))
    markup5.add(types.InlineKeyboardButton("удаление из базы", callback_data="remove"))
    return markup5

def show_message() -> dict:
    conn = sqlite3.connect('db\HTML.db', check_same_thread=False)
    cursor = conn.cursor()
    Taags = """SELECT tags, short_description FROM Tags ORDER BY id"""
    select_db = cursor.execute(Taags)
    a = {}
    for (tags, short_description) in cursor:
        a.setdefault(tags, [])
        a[tags].append(short_description)
    resultat = dict()
    for tags, short_description in select_db.fetchall():
        resultat[tags] = short_description
    print(a)
    return a

@bot.callback_query_handler(lambda call: call.data == "tomenu")
def to_menu_pressed(call: types.CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="📚список предметов📚", reply_markup=start_menu())

def start_menu() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn_list = show_message()
    for element1 in btn_list.items():
        btn = types.InlineKeyboardButton(text=element1[0], callback_data=f"address_{element1[0]}")
        markup.add(btn)
    print(element1)
    return markup

def start_menu_and_remove_btn() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    btn_list = show_message()
    for element1 in btn_list.items():
        btn_menu = types.InlineKeyboardButton(text=element1[0], callback_data=f"address_{element1[0]}")
        btn_delete = types.InlineKeyboardButton('🗑️', callback_data=f"deladdress_{element1[0]}")
        markup.add(btn_menu, btn_delete)
    return markup

@bot.callback_query_handler(lambda query: query.data.startswith("address_"))
def ans(query: types.CallbackQuery):
    global ff
    ff = query.data.split("_")[1]
    if query.data.split("_")[1]:
        bot.edit_message_text(chat_id=query.message.chat.id,  message_id=query.message.id, text=ff, reply_markup=create_pod_menu(query.data.split("_")[1]))#кнопка подменю

def pod_menu(ff) -> dict:
    conn = sqlite3.connect('db\HTML.db', check_same_thread=False)
    cursor = conn.cursor()
    sql2 = """SELECT short_description, description, sintax, photo FROM Tags WHERE tags = (?) ORDER BY id"""
    select_db2 = cursor.execute(sql2, (ff,))
    global photoresult
    global mediaresult
    photoresult = dict()
    mediaresult = dict()
    result = dict()
    for btn_name, btn_callback, media, photo in select_db2.fetchall():
        result[btn_name] = btn_callback
        photoresult[btn_name] = photo
        mediaresult[btn_name] = media
    return result

def photodict():
    btn_list4 = photoresult
    spisok_1: list = []
    for element3 in btn_list4.items():
        spisok_1.append(element3[1])

    photoindexdiapazon: list = []
    for index in range(len(spisok_1)):
        str_num = str(index)
        photoindexdiapazon.append(str_num)
    photo_dict = {photoindexdiapazon: spisok_1 for photoindexdiapazon, spisok_1 in zip(photoindexdiapazon, spisok_1)}
    return photo_dict

def mediadatadict():
    btn_list3 = mediaresult
    spisok_1: list = []
    for element3 in btn_list3.items():
        spisok_1.append(element3[1])

    mediaindexdiapazon: list = []
    for index in range(len(spisok_1)):
        str_num = str(index)
        mediaindexdiapazon.append(str_num)
    media_dict = {mediaindexdiapazon: spisok_1 for mediaindexdiapazon, spisok_1 in zip(mediaindexdiapazon, spisok_1)}
    return media_dict

def num():
    btn_list2 = pod_menu(ff)
    spisok_1: list = []
    for element3 in btn_list2.items():
        spisok_1.append(element3[0])
    indexdiapazon: list = []
    for index in range(len(spisok_1)):
        str_num = str(index)
        indexdiapazon.append(str_num)
    new_dict = {spisok_1: indexdiapazon for spisok_1, indexdiapazon in zip(spisok_1, indexdiapazon)}
    print(new_dict)
    return new_dict

def unswer_on_num():
    readydicrt = pod_menu(ff)
    dictkey = num()
    spisok_2: list = []
    for key in dictkey.items():
        spisok_2.append(key[1])
    indexdiapazon2: list = []
    for znach in readydicrt.items():
        indexdiapazon2.append(znach[1])
    finish_dict = {spisok_2: indexdiapazon2 for spisok_2, indexdiapazon2 in zip(spisok_2, indexdiapazon2)}
    print(finish_dict)
    return finish_dict

def create_pod_menu(ff) -> types.InlineKeyboardMarkup:
    markup2 = types.InlineKeyboardMarkup()
    dictkey = num()  #результат функции num
    for element in dictkey.items():
        btn = types.InlineKeyboardButton(text=element[0], callback_data=f"address2_{element[1]}")
        markup2.add(btn)
    markup2.add(types.InlineKeyboardButton("⬅ главное меню", callback_data="tomenu"))
    return markup2

@bot.callback_query_handler(lambda query2: query2.data.startswith("address2_"))
def full_descr(query2: types.CallbackQuery):#, query3: types.CallbackQuery):
    gg = query2.data.split("_")[1]  # переменная являющаяся динамично изменяемой в зависимости от того какая из кнопок нажата - по сути своей это адрес, с которым можно работать.
    itogdict = unswer_on_num() #результат функции unswer_on_num
    photo = photodict() #результат функции photodatadict
    media = mediadatadict() #результат функции mediadatadict
    answer = (itogdict[query2.data.split("_")[1]])
    photokontent = (photo[query2.data.split("_")[1]])
    mediakontent = (media[query2.data.split("_")[1]])
    access = getAccess(query2.message.chat.id)
    if photokontent != "0":
        photos = open(f'files/TG_BOT_MEDIA.DATA/' + photokontent, 'rb')
        bot.send_photo(query2.from_user.id, photos)
        photos.close()
    if mediakontent != "1":
        doc = open(f'files/TG_BOT_MEDIA.DATA/' + mediakontent, 'rb')
        bot.send_document(query2.from_user.id, doc)
        doc.close()
    bot.edit_message_text(chat_id=query2.message.chat.id,  message_id=query2.message.id, text=answer)
    if access[0] == '1':
        bot.pin_chat_message(chat_id=query2.message.chat.id, message_id=topin, disable_notification=True)  # закрепить сообщение с кнопками администратора
    bot.send_message(chat_id=query2.message.chat.id, text="текущий пункт меню: " + ff, reply_markup=create_pod_menu(ff))

def getAccess(user_id):
  with sqlite3.connect('db_login.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT user_group_id FROM users WHERE user_id=?', (user_id,))
    result = cursor.fetchone()
    return result

def add_record(tags, short_description, description, sintax, photo):
  conn = sqlite3.connect('db\HTML.db', check_same_thread=False)
  cursor = conn.cursor()
  cursor.execute('INSERT INTO Tags (tags, short_description, description, sintax, photo) VALUES (?, ?, ?, ?, ?)',
                 (tags, short_description, description, sintax, photo))
  conn.commit()

@bot.callback_query_handler(lambda call: call.data == "remove")
def get_tag(call):
    bot.send_message(call.message.chat.id, "удаление элемента в 📚список предметов📚", reply_markup=start_menu_and_remove_btn())

@bot.callback_query_handler(lambda query: query.data.startswith("deladdress_"))
def delete_files(query: types.CallbackQuery) -> dict:
    tags = query.data.split("_")[1]# адрес, с которым можно работать

    conn = sqlite3.connect('db\HTML.db', check_same_thread=False)
    cursor = conn.cursor()

    testik = """SELECT sintax, photo FROM Tags where tags = (?)"""
    select_files = cursor.execute(testik, (tags,))
    files: list = []
    spisok_files: list = []
    for allfiles in select_files.fetchall():
        files = allfiles
        for element3 in files:
            spisok_files.append(element3)


    a = spisok_files


    cursor.execute('DELETE from Tags where tags = (?)', (tags,))
    conn.commit()
    for element in a:
        if element == "1":
            continue
        if element == "0":
            continue

        if element != "0":
            if element != "1":
                file = pathlib.Path('files/TG_BOT_MEDIA.DATA/' + element)
                file.unlink()

    cursor.execute('DELETE from Tags where tags = (?)', (tags,))
    conn.commit()


@bot.callback_query_handler(lambda call: call.data == "add")
def get_tag(call):
    bot.send_message(call.from_user.id, "Введите тег: ")
    bot.register_next_step_handler(call.message, write_tag)

@bot.message_handler(content_types=['text'])
def write_tag(message):
    global tag
    tag = message.text
    bot.send_message(message.from_user.id, "Введите короткое описание: ")
    bot.register_next_step_handler(message, write_short_description)

@bot.message_handler(content_types=['text'])
def write_short_description(message):
    global short_description
    short_description = message.text
    bot.send_message(message.from_user.id, "Введите полное описание : ")
    bot.register_next_step_handler(message, write_full_description) # переход к следующим функциям (заполнение контентом save_photo, а потом media_description)

@bot.message_handler(content_types=['text'])
def write_full_description(message):
    global full_description
    full_description = message.text
    markupphoto = types.InlineKeyboardMarkup()
    markupphoto.add(types.InlineKeyboardButton("пропустить фото", callback_data="0"))
    global fotoinp
    fotoinp = bot.send_message(message.from_user.id, text="вы можете дополнить описание фотографией: ", reply_markup=markupphoto)
    if message.photo:
        bot.register_next_step_handler(message, save_photo)

@bot.callback_query_handler(lambda call: call.data == "0")
def skip_pressed(call: types.CallbackQuery):
    markupfile = types.InlineKeyboardMarkup()
    markupfile.add(types.InlineKeyboardButton("пропустить файл", callback_data="1"))
    global photo_name
    photo_name = 0
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="вы можете дополнить описание файлом: ", reply_markup=markupfile)#редактируем кнопку с предыдущего шага
    #bot.send_message(call.from_user.id, "вы можете дополнить описание файлом: ", reply_markup=markupfile)
    if call.message.document:
        bot.register_next_step_handler(call.message, media_description)

@bot.callback_query_handler(lambda call: call.data == "1")
def skip_pressed_again(call: types.CallbackQuery):
    global file_name
    file_name = 1
    in_main_menu = types.InlineKeyboardMarkup()  # добавим кнопку для возврата в главное меню
    add_record(tags=tag, short_description=short_description, description=full_description, photo=photo_name, sintax=file_name)
    in_main_menu.add(types.InlineKeyboardButton("⬅ вернуться в главное меню", callback_data="tomenu"))
    #bot.send_message(call.message.chat.id, 'данные внесены', reply_markup=in_main_menu)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='данные внесены', reply_markup=in_main_menu)#редактируем кнопку с предыдущего шага

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    global save_photo
    global photo_name
    global file_inp
    Path(f'files/TG_BOT_MEDIA.DATA/').mkdir(parents=True, exist_ok=True) # создадим папку если её нет
    markupfile = types.InlineKeyboardMarkup()
    markupfile.add(types.InlineKeyboardButton("пропустить файл", callback_data="1"))
    bot.edit_message_text(chat_id=message.chat.id, message_id=fotoinp.message_id, text="вы можете дополнить описание фотографией: ", reply_markup=None)
    file_inp = bot.send_message(message.from_user.id, "вы можете дополнить описание файлом : ", reply_markup=markupfile)
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_photo = bot.download_file(file_info.file_path)# сохраним изображение
    photo_name = file_info.file_path
    photo_way = f'files/TG_BOT_MEDIA.DATA/' + file_info.file_path
    with open(photo_way, 'wb') as new_file:
        new_file.write(downloaded_photo)
    if message.document:
        bot.register_next_step_handler(message, media_description)

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice'])# list relevant content types
def media_description(message):
    global media_description
    global file_name
    Path(f'files/TG_BOT_MEDIA.DATA/documents/').mkdir(parents=True, exist_ok=True)# создадим папку если её нет
    file_info = bot.get_file(message.document.file_id)
    file_name = file_info.file_path
    downloaded_file = bot.download_file(file_info.file_path)
    media_way = f'files/TG_BOT_MEDIA.DATA/' + file_info.file_path
    bot.edit_message_text(chat_id=message.chat.id, message_id=file_inp.message_id, text="вы можете дополнить описание файлом: ", reply_markup=None)
    in_main_menu = types.InlineKeyboardMarkup()#добавим кнопку для возврата в главное меню
    with open(media_way, 'wb') as new_file:
        new_file.write(downloaded_file)
    add_record(tags=tag, short_description=short_description, description=full_description, photo=photo_name, sintax=file_name)
    in_main_menu.add(types.InlineKeyboardButton("⬅ вернуться в главное меню", callback_data="tomenu"))
    bot.send_message(message.chat.id, 'данные внесены', reply_markup=in_main_menu)

if __name__ == '__main__':
  bot.polling(none_stop=True )


