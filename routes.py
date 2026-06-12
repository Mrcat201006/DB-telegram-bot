from email.mime import message

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import (Message , CallbackQuery, ReplyKeyboardMarkup, 
                           KeyboardButton , InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from db import add_user, get_all_users, init_db, get_user



router = Router()


class RegStates(StatesGroup):
    waiting_for_age = State()

def get_main_reply_keybord():
    keybord = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="бот туралы"), KeyboardButton(text='reg')],
            [KeyboardButton(text="users"), KeyboardButton(text="көмек")], 
        ],
        resize_keyboard=True
    )
    return keybord


@router.message(Command("start"))
async def start(message: Message):
    full_name = message.from_user.full_name
    user = await get_user(full_name)

    if user is None:
        await message.answer(
            f"Привет, {full_name}!\n"
            f"Сіз базаға қосылмаған сияқтысың.Қосылғың келсе /reg командасын қолданыңыз."
        )
    else:
        await message.answer(
            f"Сәлем сен базға қосылғансын!\n"
            f"Есімін:{user[1]}\n"
            f"Жасын:{user[2]}\n"
            "Көмек керек болса /help командасын қолданыңыз."
            
        )
        

@router.message(Command('help'))
@router.message(F.text.lower() == "көмек")
async def help(message: Message):
    await message.answer(
        "Командалар:\n /help - команда тізімі\n /about - бот сипаттамасы\n /reg - базаға қосылу\n /users - базадағы барлық қолданушылар көру",
        reply_markup=get_main_reply_keybord()
    )
    
    
@router.message(Command("about"))
@router.message(F.text.lower() == "бот туралы")
async def about(message: Message):
    await message.answer("Бұл бот регестрация командасын қолданылуын көрсету үшін арналған")
    
    
@router.message(Command("users"))
async def users (message: Message):
    users = await get_all_users()
        
    if not users:
        await message.answer ("В базе нет пользователей")
        return
    
    text = "Пользователи в базе:\n\n"
    for id, full_name, age in users:
        text += f"ID: {id}, Есім: {full_name}, Жасы: {age}\n"
    await message.answer(text)
            
@router.message(Command("reg"))
@router.message(F.text.lower() == "reg")
async def reg(message: Message, state: FSMContext):
    user = await get_user(message.from_user.full_name)
    if user:
        await message.answer("Сен базада бұрыннан барсың!")
        return

    await message.answer("Жасыңды жаз:")
    await state.set_state(RegStates.waiting_for_age)

@router.message()
async def save_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Жасыңды дұрыс жаз! Сан түрінде болуы керек.")
        return

    user = await get_user(message.from_user.full_name)

    if user:
        await message.answer("Сен базада бұрыннан барсың!")
        return

    age = int(message.text)
    await add_user(
        message.from_user.full_name,
        age
    )

    await message.answer("Тіркеу аяқталды!")
    await state.clear()
    

