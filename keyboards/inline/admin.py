from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.connections import admin_get_all_products, get_all_admins, get_bot_configs, get_all_channels


async def admin_menu_btn():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(text='💵 Изменить цены', callback_data='admin:change_prices'),
        InlineKeyboardButton(text='📮 Рассылка юзерам', callback_data='admin:sending_msg'),
        InlineKeyboardButton(text='👥 Список админов', callback_data='admin:all_admins'),
        InlineKeyboardButton(text='📢 Каналы', callback_data='admin:channels'),
    )
    keyboard.adjust(2)
    return keyboard.as_markup()


async def admin_manage_btn(is_url: bool = None, is_manage: bool = False):
    keyboard = InlineKeyboardBuilder()
    admins = await get_all_admins()
    if is_url:
        keyboard.add(
            *[InlineKeyboardButton(text=f"👨🏻‍💻 {item['admin_fullname']}",
                                   url=f"tg://user?id={item['admin_id']}") for
              item in admins]
        )
    elif is_url is False:
        keyboard.add(
            *[InlineKeyboardButton(text=f"👨🏻‍💻 {item['admin_fullname']}",
                                   callback_data=f"admin_manage:{item['admin_id']}")
              for item in admins]
        )
    keyboard.adjust(2)
    if is_manage:
        keyboard.row(
            InlineKeyboardButton(text='➕ Добавить', callback_data='admin_manage:plus'),
            InlineKeyboardButton(text='➖ Удалить', callback_data='admin_manage:minus'),
        )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data=f"admin_manage:back"),
    )
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


async def admin_edit_products_btn():
    products = InlineKeyboardBuilder()
    all_products = await admin_get_all_products()
    bot_configs = await get_bot_configs()
    products.add(
        *[InlineKeyboardButton(text=f"{item['name']} | {item['price']} руб", callback_data=f"edit_price:{int(item['id'])}") for item in all_products],
    )
    products.row(
        InlineKeyboardButton(text=f"Реф.сум | {bot_configs[-1]['ref_sum']} руб", callback_data=f"edit_price:config:ref_sum"),
        InlineKeyboardButton(text=f"Мин сум п.счета | {bot_configs[-1]['min_sum']} руб", callback_data=f"edit_price:config:min_sum")
    )
    products.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="admin_manage:back")
    )
    products.adjust(1)
    return products.as_markup()


async def get_all_channels_btn(just_show: bool = False, manage_channel: bool = False, with_callback: bool = False):
    channels = await get_all_channels()
    keyboard = InlineKeyboardBuilder()
    if just_show:
        keyboard.add(
            *[InlineKeyboardButton(text=f"{item['channel_name']}", url=f"{item['channel_url']}") for item in channels]
        )
    if with_callback:
        keyboard.add(
            *[InlineKeyboardButton(text=f"{item['channel_name']}", callback_data=f"channel_manage:{item['channel_id']}") for item in channels]
        )
    keyboard.adjust(1)
    if manage_channel:
        keyboard.row(
            InlineKeyboardButton(text='➕ Добавить', callback_data='channel_manage:plus'),
            InlineKeyboardButton(text='➖ Удалить', callback_data='channel_manage:minus'),
        )
    keyboard.row(
        InlineKeyboardButton(text="🔙 Назад", callback_data="admin_manage:back")
    )
    return keyboard.as_markup()

