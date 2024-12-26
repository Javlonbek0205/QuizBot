import aiosqlite
from typing import List
import asyncio



class Question:
    def __init__(self, question: str, options: List[str], correct_option_id: int, level: str, explanation: str,
                 time_given: int):
        self.question = question
        self.options = options
        self.correct_option_id = correct_option_id
        self.level = level
        self.explanation = explanation
        self.time_given = time_given


class QuestionDatabase:
    def __init__(self, db_path='database/questions1.db'):
        self.db_path = db_path

    async def initialize(self):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(''' 
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    options TEXT,
                    correct_option_id INTEGER,
                    level TEXT,
                    explanation TEXT,
                    time_given INTEGER
                )   
            ''')
            await db.commit()

    async def add_question(self, question: Question):
        options_str = ';'.join(question.options)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                INSERT INTO questions (question, options, correct_option_id, level, explanation, time_given)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (question.question, options_str, question.correct_option_id, question.level, question.explanation,
                  question.time_given))
            await db.commit()

    async def get_questions(self, level=None):
        async with aiosqlite.connect(self.db_path) as db:
            # Savollarni tanlang
            if level:
                cursor = await db.execute('SELECT * FROM questions WHERE level = ?', (level,))
            else:
                cursor = await db.execute('SELECT * FROM questions')

            rows = await cursor.fetchall()

            if not rows:  # Agar hech qanday natija bo'lmasa
                return []

            questions = []
            for row in rows:
                try:
                    # Har bir qatorni `Question` obyektiga aylantirish
                    options = row[2].split(';') if row[2] else []  # Bo'sh bo'lsa, bo'sh ro'yxat
                    question = Question(
                        question=row[1],
                        options=options,
                        correct_option_id=row[3],
                        level=row[4],
                        explanation=row[5] if len(row) > 5 else None,  # Xatoga qarshi tekshirish
                        time_given=row[6] if len(row) > 6 else None  # Xatoga qarshi tekshirish
                    )
                    questions.append(question)
                except IndexError as e:
                    print(f"Row parsing error: {e}. Row data: {row}")
                    continue

            return questions

    async def add_sample_questions(self):
        questions = await self.get_questions()
        if not questions:
            question1 = Question(
                question="What is the capital of Japan?",
                options=["Beijing", "Seoul", "Tokyo", "Bangkok"],
                correct_option_id=2,
                level="medium",
                explanation="Tokyo is the capital of Japan.",
                time_given=30
            )

            question2 = Question(
                question="What is the square root of 64?",
                options=["6", "7", "8", "9"],
                correct_option_id=2,
                level="medium",
                explanation="The square root of 64 is 8.",
                time_given=30
            )

            question3 = Question(
                question="Which planet is known as the Red Planet?",
                options=["Earth", "Mars", "Jupiter", "Saturn"],
                correct_option_id=1,
                level="medium",
                explanation="Mars is known as the Red Planet.",
                time_given=30
            )

            question4 = Question(
                question="What is the boiling point of water in Celsius?",
                options=["80°C", "90°C", "100°C", "110°C"],
                correct_option_id=2,
                level="medium",
                explanation="The boiling point of water is 100°C.",
                time_given=30
            )

            question5 = Question(
                question="Who developed the theory of relativity?",
                options=["Isaac Newton", "Albert Einstein", "Galileo Galilei", "Nikola Tesla"],
                correct_option_id=1,
                level="medium",
                explanation="Albert Einstein developed the theory of relativity.",
                time_given=30
            )
            await self.add_question(question1)
            await self.add_question(question2)
            await self.add_question(question3)
            await self.add_question(question4)
            await self.add_question(question5)
            print("new questions added")
        else:
            print("questions already exists")


async def create_questions():
    db = QuestionDatabase()
    await db.initialize()
    await db.add_sample_questions()