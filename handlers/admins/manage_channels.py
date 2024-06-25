from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from peewee import DataError, IntegrityError

from database.connections import get_all_admins, add_channel, delete_channel
from filters.is_admin import IsAdmin
from keyboards.inline.admin import get_all_channels_btn
from states.admin_states import Admin
from utils.bot_context import add_channel_text
from utils.misc.useful_functions import get_admin_context
from loader import bot

router = Router()


@router.callback_query(F.data == "admin:channels", IsAdmin())
async def handle_admin(call: CallbackQuery):
    data = call.data.split(":")[1]
    btn = await get_all_channels_btn(just_show=True, manage_channel=True)
    await call.message.edit_text("📢 Каналы", reply_markup=btn)


@router.callback_query(F.data.startswith("channel_manage:"), IsAdmin())
async def handle_admin_manage(call: CallbackQuery, state: FSMContext):
    data = call.data.split(":")[1]
    user_id = call.from_user.id
    if data == "plus":
        await call.message.delete()
        btn = await get_all_channels_btn(manage_channel=True)
        await call.message.answer(add_channel_text, reply_markup=btn)
        await state.set_state(Admin.add_channel_state)
    elif data == "minus":
        await call.message.delete()
        btn = await get_all_channels_btn(with_callback=True)
        await call.message.answer("Выберите для удаления", reply_markup=btn)
    elif int(data) < 0:
        await delete_channel(int(data))
        await call.answer("Успешно удален", show_alert=True)
        await call.message.delete()
        context, btn = await get_admin_context()
        await call.message.answer(context, reply_markup=btn)


@router.message(Admin.add_channel_state, IsAdmin())
async def add_admin_handler(message: Message, state: FSMContext):
    text = message.text
    data = text.split(" + ")
    if len(data) < 2:
        btn = await get_all_channels_btn(manage_channel=True)
        await message.answer(add_channel_text, reply_markup=btn)
        return
    channel_id, channel_name, channel_url = data[0], data[1], data[2]
    try:
        await add_channel(int(channel_id), channel_name, channel_url)
    except DataError:
        await message.answer("Что-то пошло не так ❌")
        btn = await get_all_channels_btn(manage_channel=True)
        await message.answer(add_channel_text, reply_markup=btn)
        return
    except IntegrityError:
        await message.answer("Такой канал уже есть ❌")
        btn = await get_all_channels_btn(manage_channel=True)
        await message.answer(add_channel_text, reply_markup=btn)
        return

    # await message.delete()
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id - 1)
    await message.answer("Успешно добавлен ✅")
    await state.clear()
    context, btn = await get_admin_context()
    await message.answer(context, reply_markup=btn)
