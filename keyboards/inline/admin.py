from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.connections import get_all_admins


async def admin_menu_btn():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text='💵 Изменить цены', callback_data='admin:change_prices'),
        InlineKeyboardButton(text='📮 Рассылка юзерам', callback_data='admin:sending_msg'),
        InlineKeyboardButton(text='👥 Список админов', callback_data='admin:all_admins')
    )
    keyboard.adjust(2)
    return keyboard.as_markup()


async def admin_manage_btn():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text='➕ Добавить', callback_data='admin_manage:plus'),
        InlineKeyboardButton(text='➖ Удалить', callback_data='admin_manage:minus'),
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data=f"admin_manage:back"),
    )
    keyboard.adjust(2)
    return keyboard.as_markup()


async def admin_list_btn():
    keyboard = InlineKeyboardBuilder()
    admins = await get_all_admins()
    keyboard.add(
        *[InlineKeyboardButton(text=f"{item['admin_fullname']}") for item in admins]
    )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data=f"admin_manage:back"),
    )
    keyboard.adjust(2)
    return keyboard.as_markup()
