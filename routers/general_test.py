from aiogram import Router, Dispatcher
from aiogram.types import Message, PollAnswer
from aiogram.filters import Command
from database.question_db import QuestionDatabase
from tests.quetions_db_test import questions  # Savollarni yuklash
from aiogram.fsm.context import FSMContext

exam_router = Router()

async def handle_state(message: Message, state: FSMContext):
    await state.update_data(cur_question_index=0)
    await state.update_data(correct_answers=0)
    await create_poll(message=message, state=state)

async def create_poll(message: Message, state: FSMContext):
    data = await state.get_data()  # Holat ma'lumotlarini oling
    i = data.get('cur_question_index')  # 'cur_question_index' ni oling
    if i is None:  # Agar mavjud bo'lmasa, default qiymat 0 bo'lsin
        i = 0

    db = QuestionDatabase()
    questions = await db.get_questions(level="medium")
    if not questions:  # Savollar bo'sh bo'lsa
        await message.answer("No questions found in the database!")
        return

    if i >= len(questions):  # Indeks savollar ro'yxati chegarasidan oshmasligini tekshiring
        await message.answer("All questions have been answered!")
        return

    question = questions[i]  # Savolni oling
    poll_message = await message.answer_poll(
        question=question.question,
        options=question.options,
        correct_option_id=question.correct_option_id,
        explanation=question.explanation,
        open_period=question.time_given,
        is_anonymous=False,
        type='quiz'
    )

    # Holatni yangilang
    await state.update_data(message=message)
    await state.update_data(chat_id=poll_message.chat.id)
    await state.update_data(correct_option_id=question.correct_option_id)

async def handle_poll(poll_answer: PollAnswer, state: FSMContext):
    # Barcha holat ma'lumotlarini oling
    data = await state.get_data()

    # Tanlangan javobni oling
    picked_option = poll_answer.option_ids[0]
    correct_answer_count = data.get("correct_answers", 0)  # Agar mavjud bo'lmasa, 0 bo'lsin

    # To'g'ri javobni tekshirish
    if picked_option == data["correct_option_id"]:
        correct_answer_count += 1
        await state.update_data(correct_answers=correct_answer_count)

    # Savol indeksini yangilang
    updated_question_index = data.get("cur_question_index", 0)  # Default qiymat 0
    updated_question_index += 1
    await state.update_data(cur_question_index=updated_question_index)

    # Foydalanuvchi ma'lumotlarini olish
    message = data.get("message")
    level = "medium"
    db = QuestionDatabase()
    questions = await db.get_questions(level=level)

    # Yangi savol yuborish yoki natijani chiqarish
    if updated_question_index < len(questions):
        await create_poll(message, state)
    else:
        chat_id = data.get("chat_id")
        if chat_id:
            await poll_answer.bot.send_message(
                chat_id,
                f"Sizning natijangiz: {correct_answer_count}/{len(questions)}"
            )


def register_general(dp: Dispatcher):
    dp.message.register(handle_state, Command('start'))
    dp.message.register(create_poll, Command('start'))
    dp.poll_answer.register(handle_poll)


