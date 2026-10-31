from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.db import get_tasks, add_task, delete_task

router = Router()

@router.message(F.text == "ℹ️ Help")
async def helper_btn(message: Message):
    await message.answer("Send <b>➕ Add Task</b> or use the command menu to get started.", parse_mode="HTML")

@router.message(F.text == "📋 My Tasks")
async def list_tasks(message: Message):
    tasks = await get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("📭 You have no pending tasks. Enjoy your free time!")
        return
    
    text = "📋 <b>Your Tasks:</b>\n\n"
    for task_id, title in tasks:
        text += f"• {title}\n"
        
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"❌ Delete: {title[:15]}...", callback_data=f"del_{task_id}")] for task_id, title in tasks
    ])
    
    await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

@router.message(F.text == "➕ Add Task")
async def prompt_add_task(message: Message):
    await message.answer("Please send the title of the task you want to add (e.g., <i>Buy groceries</i>)", parse_mode="HTML")

@router.message(F.text & ~F.text.startswith("/"))
async def handle_new_task_text(message: Message):
    if message.text in ["📋 My Tasks", "➕ Add Task", "ℹ️ Help"]:
        return
    await add_task(message.from_user.id, message.text)
    await message.answer(f"✅ Task added successfully:\n<b>{message.text}</b>", parse_mode="HTML")

@router.callback_query(F.data.startswith("del_"))
async def process_delete_task(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    await delete_task(task_id)
    await callback.answer("Task deleted!")
    await callback.message.edit_text("🗑️ Task has been deleted.")