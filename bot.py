from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from PIL import Image
import bot_text as txt
from enum import Enum

class VoiceMessage(str, Enum):
    LOVE = 'love'
    CHAT_GPT = 'chat_gpt'
    SQL = 'sql'

class ImageMessage(str, Enum):
    LAST_SELFI = 'last_selfi'
    HIGH_SCHOOL = 'high_school'


class MyBot(TeleBot):
    def _create_multichoice(self, answers: dict[str, str]) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup()
        for btn, name in answers.items():
            key = InlineKeyboardButton(text=name, callback_data=btn)
            keyboard.add(key)
        return keyboard
    def send_photo_answer(self, message: Message, photo_type: ImageMessage) -> None:
        if photo_type == ImageMessage.LAST_SELFI:
            self.send_photo(
                  message.from_user.id,
                  photo=Image.open('./media/selfi.jpg'),
                  caption=txt.LAST_SELFI_CAPTION
              )
        if photo_type == ImageMessage.HIGH_SCHOOL:
            self.send_photo(
                  message.from_user.id,
                  photo=Image.open('./media/school.jpg'),
                  caption=txt.HIGH_SCHOOL_CAPTION
              )
    def send_audio_message(self, message: Message, voice_type: VoiceMessage) -> None:
        if voice_type == VoiceMessage.CHAT_GPT:
          self.send_voice(
              message.from_user.id,
              voice=open('./media/GPT.m4a', 'rb'),
              caption=txt.GPT_CAPTION
          )
        elif voice_type == VoiceMessage.SQL:
            self.send_voice(
              message.from_user.id,
              voice=open('./media/SQL.m4a', 'rb'),
              caption=txt.SQL_CAPTION
          )
        elif voice_type == VoiceMessage.LOVE:
            self.send_voice(
              message.chat.id,
              voice=open('./media/Love.m4a', 'rb'),
              caption=txt.LOVE_CAPTION
          )
    def send_welcome(self, message: Message) -> None:
        self.send_message(
            message.from_user.id,
            text=txt.WELCOME_MESSAGE,
        )
        self.send_message(
            message.from_user.id,
            text=txt.WELCOME_QUESTION,
            reply_markup=self._create_multichoice(answers = txt.WELCOME_CHOICE)
        )
    def send_about(self, message: Message) -> None:
        self.send_message(
            message.chat.id,
            text=txt.ABOUT_MESSAGE,
        )
        self.send_message(
            message.chat.id,
            text=txt.ABOUT_QUESTION,
            reply_markup=self._create_multichoice(answers = txt.ABOUT_CHOICE)
        )
    def resend_message(self, message):
        self.send_message(
            txt.CHAT_ID,
            text=message.text,
        )
        self.send_message(
            message.from_user.id,
            text=txt.NEXT_STEP_DONE,
        )


bot = MyBot(txt.TOKEN)

@bot.message_handler(commands=["start", "welcome"])
def send_help(message):
    bot.send_welcome(message)

@bot.message_handler(commands=["help", "nextstep", "last_selfi", "high_school", "chat_gpt", "sql"])
def send_answer(message):
    match message.text:
        case '/help':
            bot.reply_to(message, txt.HELP_MESSAGE)
        case '/nextstep':
            bot.reply_to(message, txt.NEXT_STEP_MESSAGE)
            bot.register_next_step_handler(message, bot.resend_message)
        case '/last_selfi':
            bot.send_photo_answer(message, ImageMessage.LAST_SELFI)
        case '/high_school':
            bot.send_photo_answer(message, ImageMessage.HIGH_SCHOOL)
        case '/chat_gpt':
            bot.send_audio_message(message, VoiceMessage.CHAT_GPT)
        case '/sql':
            bot.send_audio_message(message, VoiceMessage.SQL)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    match call.data:
        case "about":
            bot.send_about(call.message)
        case "backend":
            bot.send_message(call.message.chat.id, text=txt.BACKEND_MESSAGE)
        case "hobby":
            bot.send_message(call.message.chat.id, text=txt.HOBBY_MESSAGE)
        case "love":
            bot.send_audio_message(call.message, VoiceMessage.LOVE)
        case "photo":
            bot.send_message(call.message.chat.id, text=txt.PHOTO_MESSAGE)
        case "tech":
            bot.send_message(call.message.chat.id, text=txt.TECH_MESSAGE);
        case "code":
            bot.send_message(call.message.chat.id, text=txt.CODE_MESSAGE);

@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)
