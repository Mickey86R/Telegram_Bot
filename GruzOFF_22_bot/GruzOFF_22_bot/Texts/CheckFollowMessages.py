from aiogram.utils.markdown import text

from emoji import emojize

isFollow = emojize(text('Приветствую! \N{raised hand} Это Бот Телеграм канала "GruzOff" Услуги Профессионалов.',
                'В нём можно создать заказ для телеграмм канала, узнать всю нужную информацию, правила и не только.',
                'Нажми кнопку "Главное меню", чтобы перейти к использованию Бота. \N{winking face}', sep = "\n"))

isNotFollow = emojize(text('К сожалению, вы не являетесь участником канала "GruzOFF". \N{confused face} ',
                'Чтобы подписаться, вам нужно обратиться к создателю канала Николаю ( @kalyan_pergament ), либо к главному Администратору Матвею ( @I_am_banann ), они будут проводить вам собеседование по результатам которого вы сможете стать участником. Желаю удачи! \N{flexed biceps}', sep = "\n"))