from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 My Tasks"), KeyboardButton(text="➕ Add Task")],
            [KeyboardButton(text="ℹ️ Help")]
        ],
        resize_keyboard=True
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Welcome, <b>{message.from_user.full_name}</b>!\n\n" 
        "I am <b>TaskMaster Pro</b>, your personal productivity bot.\n" 
        "Use the keyboard below to manage your tasks.",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "📖 <b>Help Guide</b>\n\n" 
        "- <b>📋 My Tasks</b>: View your pending tasks\n" 
        "- <b>➕ Add Task</b>: Create a new task\n" 
        "Type naturally or use buttons to interact.",
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )