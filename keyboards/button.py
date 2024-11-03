from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from messages import TEXT_B_REMOVE, TEXT_B_MUSIC, TEXT_B_NEEDLE_WORK, TEXT_B_FORM, TEXT_B_CONFIRM, TEXT_B_AWARDS, TEXT_B_ADMIN, TEXT_B_ADD_AWARDS, TEXT_B_FULFILL_AWARDS, TEXT_B_DEFER_AWARDS, TEXT_B_AWARDS_ACTION, TEXT_B_MESSAGE_TEMPLATES,TEXT_B_AWARDS_BOOK, TEXT_B_AWARDS_GAME,TEXT_B_AWARDS_VIEWING, TEXT_B_AWARDS_ARTICLE, TEXT_B_EVENT, TEXT_B_SUBSCRIBE, TEXT_B_ADD_SCHEDULE, TEXT_B_VIEW_SCHEDULE, TEXT_B_CARD, TEXT_B_VIEW_EVENT_2

def main_kb(username: str, admin_username: list[str]):
    kb_list = [
        [KeyboardButton(text=TEXT_B_FORM)],
        [KeyboardButton(text=TEXT_B_EVENT), KeyboardButton(text=TEXT_B_MUSIC)],
        [KeyboardButton(text=TEXT_B_VIEW_EVENT_2)],
        [KeyboardButton(text=TEXT_B_AWARDS), KeyboardButton(text=TEXT_B_VIEW_SCHEDULE)],
        [KeyboardButton(text=TEXT_B_SUBSCRIBE)]
    ]
    if username in admin_username:
        kb_list.append([KeyboardButton(text=TEXT_B_ADMIN)])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def choice_kb(kb_confirm: bool = False):
    kb_choice_list = [
        [KeyboardButton(text=TEXT_B_REMOVE)]
    ]
    if kb_confirm:
        kb_choice_list.append([KeyboardButton(text=TEXT_B_CONFIRM)])
    keyboard = ReplyKeyboardMarkup(keyboard=kb_choice_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def admin_kb():
    kb_admin_list = [
        [KeyboardButton(text=TEXT_B_AWARDS_ACTION), KeyboardButton(text=TEXT_B_MESSAGE_TEMPLATES)],
        [KeyboardButton(text=TEXT_B_ADD_SCHEDULE)],
        [KeyboardButton(text=TEXT_B_REMOVE)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_admin_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def award_actions_kb():
    kb_award_actions_list = [
        [KeyboardButton(text=TEXT_B_ADD_AWARDS)], 
        [KeyboardButton(text=TEXT_B_DEFER_AWARDS), KeyboardButton(text=TEXT_B_FULFILL_AWARDS)],
        [KeyboardButton(text=TEXT_B_AWARDS)],
        [KeyboardButton(text=TEXT_B_REMOVE)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_award_actions_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def check_subscription_kb():
    kb_check_subscription = [[KeyboardButton(text="/start")]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_check_subscription, resize_keyboard=True, one_time_keyboard=True)
    return keyboard

def award_list_kb():
    kb_award_list = [
        [KeyboardButton(text=TEXT_B_AWARDS_BOOK), KeyboardButton(text=TEXT_B_AWARDS_ARTICLE), KeyboardButton(text=TEXT_B_CARD)], 
        [KeyboardButton(text=TEXT_B_AWARDS_GAME), KeyboardButton(text=TEXT_B_AWARDS_VIEWING)],
        [KeyboardButton(text=TEXT_B_REMOVE)]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb_award_list, resize_keyboard=True, one_time_keyboard=True)
    return keyboard