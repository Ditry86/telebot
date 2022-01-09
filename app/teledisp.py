import os
from queue import Queue

from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
from flask import current_app
#from app import db


# from pyrogram import Client


def init_bot_webhook(BOT_TOKEN, HOST_URL, HOST_IP, CERT):
    bot = Bot(BOT_TOKEN)
    #result = bot.setWebhook(url=HOST_URL + BOT_TOKEN, certificate=open(CERT, 'r'))
    result = bot.setWebhook(url=HOST_URL + BOT_TOKEN)
    return bot, result


# def make_bot_client()


def init_upd_dispatcher(bot):
    disp = Dispatcher(bot, Queue())

    def start(update: Update):
        # Init user object variables
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        chat_id = update.effective_chat.id
        profile_photos = update.effective_user.get_profile_photos()
        prof_photo_file = profile_photos.photos[0][0].get_file()
        full_path = os.path.join(current_app.root_path, 'media', prof_photo_file.file_id)
        # Create user with check
        with current_app.app_context():
            check_user = db.User.query.filter_by(id=user_id)
            if check_user is None:
                new_user = db.User(id=user_id, name=user_name, chat_id=chat_id,
                                   photho_id=prof_photo_file.file_id, photo_path=full_path)
                try:
                    if os.path.isfile(full_path):
                        os.remove(full_path)
                except FileNotFoundError:
                    print('Create new prof. photo file (' + prof_photo_file.file_id + ') for user '
                          + user_name + ' (' + user_id + ')')
                prof_photo_file.download(full_path)
                new_user.add()
            else:
                update.message.reply_text('You are already registered!')
        update.message.reply_text('Hello ' + user_name + '! You register with your ID -'
                                  + str(user_id))

    def me(update: Update):
        # Check user
        # _________
        # If user is in DB, add this user to DB
        # _________
        update.message.reply_text(update.effective_user.first_name + '. Your ID - ' + str(update.effective_user.id))
        photos = update.effective_user.get_profile_photos()
        photo_id = photos.photos[0][0].file_id
        # photo_file = photos.photos[0][0].get_file()
        update.message.reply_photo(photo_id)

    # def clear(update: Update, context: CallbackContext):

    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CommandHandler('me', me))
    return disp
