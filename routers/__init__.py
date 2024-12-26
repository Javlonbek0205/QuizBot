from aiogram import Dispatcher
from .start import register_start
from .level_test import register_level
from .general_test import register_general


def register_routers(dp: Dispatcher):
    register_start(dp)
    register_level(dp)
    register_general(dp)

