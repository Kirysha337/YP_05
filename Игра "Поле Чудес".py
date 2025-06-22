from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QLineEdit, QWidget, QMessageBox, QStackedWidget, QGridLayout,
    QFrame, QInputDialog, QDialog
)
from PyQt5.QtGui import QPixmap, QTransform, QFont
from PyQt5.QtCore import Qt, QTimer
import random

class VictoryDialog(QDialog):
    def __init__(self, score, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Победа!")
        self.setFixedSize(400, 300)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #e8d5c4;
            }
            QLabel {
                color: #2d3436;
                font-size: 18px;
                font-weight: bold;
                text-shadow: 1px 1px 2px #ffffff;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 15px;
                border-radius: 10px;
                color: #2d3436;
                min-width: 130px;
                margin: 5px;
                background-color: #eed6c4;
                border: 2px solid #9e7676;
            }
            QPushButton:hover {
                background-color: #ffd6c4;
                border-color: #815b5b;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)  # Добавляем отступы от краев окна

        # Текст поздравления
        congrats_label = QLabel("🎉 Поздравляем! 🎉\nВы победили!")
        congrats_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(congrats_label)

        # Показываем набранные очки
        score_label = QLabel(f"Ваши очки: {score}")
        score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(score_label)

        # Контейнер для кнопок
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(15)  # Уменьшаем отступ между кнопками
        button_layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы у контейнера кнопок

        # Кнопка "Играть снова"
        play_again_btn = QPushButton("Играть снова")
        play_again_btn.setFixedWidth(150)  # Фиксированная ширина кнопки
        play_again_btn.setObjectName("play_again")
        play_again_btn.clicked.connect(self.accept)
        button_layout.addWidget(play_again_btn)

        # Кнопка "Выйти из игры"
        exit_btn = QPushButton("Выйти из игры")
        exit_btn.setFixedWidth(150)  # Фиксированная ширина кнопки
        exit_btn.setObjectName("exit_game")
        exit_btn.clicked.connect(self.reject)
        button_layout.addWidget(exit_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

class PoleChudesGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поле Чудес")
        self.setGeometry(100, 100, 800, 600)

        # Слова и вопросы для разных уровней сложности
        self.words_with_questions = {
            "Легкий": [
                {"word": "КОД", "question": "Последовательность инструкций для компьютера"},
                {"word": "БИТ", "question": "Минимальная единица информации"},
                {"word": "ЧАТ", "question": "Онлайн-общение в реальном времени"},
                {"word": "САЙТ", "question": "Веб-страница в интернете"},
                {"word": "ТЕГ", "question": "Элемент разметки в HTML"},
                {"word": "ЛИНК", "question": "Ссылка на другую страницу"},
                {"word": "БАГ", "question": "Ошибка в программе"},
                {"word": "ФАЙЛ", "question": "Единица хранения данных на компьютере"},
                {"word": "ПОРТ", "question": "Точка подключения в сети"},
                {"word": "ЛОГ", "question": "Журнал событий системы"},
                {"word": "КЛИК", "question": "Нажатие кнопки мыши"},
                {"word": "ЮЗЕР", "question": "Пользователь системы"},
                {"word": "ПИН", "question": "Код для доступа или идентификации"},
                {"word": "БИТЫ", "question": "Множественное число минимальных единиц информации"},
                {"word": "ХЭШ", "question": "Результат хеширования данных"}
            ],
            "Средний": [
                {"word": "ПИТОН", "question": "Популярный язык программирования с символом змеи"},
                {"word": "СЕРВЕР", "question": "Компьютер, предоставляющий ресурсы по сети"},
                {"word": "БРАУЗЕР", "question": "Программа для просмотра веб-страниц"},
                {"word": "АЛГОРИТМ", "question": "Последовательность шагов для решения задачи"},
                {"word": "ПРОТОКОЛ", "question": "Набор правил для передачи данных"},
                {"word": "КЛАВИША", "question": "Элемент клавиатуры"},
                {"word": "ПАКЕТ", "question": "Единица передачи данных в сети"},
                {"word": "СОКЕТ", "question": "Интерфейс для обмена данными между процессами"},
                {"word": "ОПЕРАЦИЯ", "question": "Действие, выполняемое программой"},
                {"word": "ПАРОЛЬ", "question": "Секретный набор символов для входа"},
                {"word": "МОДУЛЬ", "question": "Часть программы, выполняющая отдельную функцию"},
                {"word": "ПАМЯТЬ", "question": "Ресурс для хранения данных в компьютере"},
                {"word": "СЕТЬ", "question": "Объединение компьютеров для обмена данными"},
                {"word": "ДИСК", "question": "Устройство для хранения информации"},
                {"word": "КЛАСС", "question": "Структура данных в объектно-ориентированном программировании"}
            ],
            "Сложный": [
                {"word": "ПРОГРАММИСТ", "question": "Человек, который пишет код"},
                {"word": "ИНТЕРФЕЙС", "question": "Способ взаимодействия пользователя с программой"},
                {"word": "БАЗАДАННЫХ", "question": "Организованное хранилище информации"},
                {"word": "ВИРТУАЛИЗАЦИЯ", "question": "Технология создания виртуальных ресурсов"},
                {"word": "ИНКАПСУЛЯЦИЯ", "question": "Сокрытие деталей реализации в ООП"},
                {"word": "ПОЛИМОРФИЗМ", "question": "Способность объекта принимать разные формы"},
                {"word": "РЕФАКТОРИНГ", "question": "Процесс улучшения кода без изменения функционала"},
                {"word": "ДЕБАГГИНГ", "question": "Процесс поиска и устранения ошибок"},
                {"word": "КОНСТРУКТОР", "question": "Специальный метод для создания объекта"},
                {"word": "ИНТЕРПРЕТАТОР", "question": "Программа, выполняющая код построчно"},
                {"word": "КОМПИЛЯТОР", "question": "Программа, переводящая код в машинный язык"},
                {"word": "МУЛЬТИЗАДАЧНОСТЬ", "question": "Выполнение нескольких задач одновременно"},
                {"word": "СЕРИАЛИЗАЦИЯ", "question": "Преобразование объекта в поток байтов"},
                {"word": "ДЕССЕРИАЛИЗАЦИЯ", "question": "Восстановление объекта из потока байтов"},
                {"word": "КИБЕРБЕЗОПАСНОСТЬ", "question": "Защита информации и систем от атак"}
            ]
        }
        
        # Текущие игровые данные
        self.current_word_data = None
        self.hidden_word = ""
        self.guessed_word = []
        
        # Сектора барабана
        self.sectors = {
            "Легкий": ["+100", "+200", "+300", "+500", "Приз", "+400"],
            "Средний": ["+200", "+400", "+600", "+800", "Банкрот", "+1000"],
            "Сложный": ["+300", "+600", "+900", "+1200", "Банкрот", "+1500"]
        }
        
        # Очки игрока и состояние игры
        self.total_score = 0
        self.difficulty = None
        self.current_spin_result = None
        self.can_guess = False
        self.current_potential_score = 0

        # Таймер для вращения барабана
        self.spin_timer = QTimer()
        self.spin_angle = 0
        self.spin_timer.timeout.connect(self.update_wheel_rotation)

        # Создание интерфейса
        self.init_ui()

    def init_ui(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Загрузочный экран с выбором сложности
        self.create_start_screen()
        
        # Экран игры
        self.create_game_screen()

    def create_start_screen(self):
        start_widget = QWidget()
        layout = QVBoxLayout()
        start_widget.setLayout(layout)

        # Установка фонового изображения через стиль
        start_widget.setStyleSheet("""
            background-image: url('background.jpg'); 
            background-repeat: no-repeat; 
            background-position: center; 
            background-size: cover;
        """)

        # Приветственное сообщение
        welcome_label = QLabel("Добро пожаловать в игру 'Поле Чудес'!")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2d3436;
            margin-bottom: 30px;
            text-shadow: 1px 1px 2px #ffffff;
        """)
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        layout.addWidget(welcome_label)

        # Выбор сложности
        difficulty_label = QLabel("Выберите уровень сложности:")
        difficulty_label.setAlignment(Qt.AlignCenter)
        difficulty_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #2d3436;
            margin-bottom: 20px;
            text-shadow: 1px 1px 2px #ffffff;
        """)
        layout.addWidget(difficulty_label)

        # Кнопки сложности
        button_style = """
            QPushButton {
                font-size: 16px; 
                padding: 12px; 
                margin: 8px 120px; 
                border-radius: 10px; 
                background-color: #e8d5c4; 
                color: #2d3436;
                min-width: 200px;
                border: 2px solid #9e7676;
            }
            QPushButton:hover {
                background-color: #eed6c4;
                border-color: #815b5b;
            }
        """

        easy_btn = QPushButton("Легкий")
        medium_btn = QPushButton("Средний")
        hard_btn = QPushButton("Сложный")

        for btn in [easy_btn, medium_btn, hard_btn]:
            btn.setStyleSheet(button_style)
            btn.setFont(QFont("Arial", 12, QFont.Bold))
            layout.addWidget(btn)

        easy_btn.clicked.connect(lambda: self.start_game("Легкий"))
        medium_btn.clicked.connect(lambda: self.start_game("Средний"))
        hard_btn.clicked.connect(lambda: self.start_game("Сложный"))

        self.stacked_widget.addWidget(start_widget)

    def create_game_screen(self):
        game_widget = QWidget()
        game_layout = QVBoxLayout()
        game_widget.setLayout(game_layout)

        game_widget.setStyleSheet("""
            background-image: url('background.jpg'); 
            background-repeat: no-repeat; 
            background-position: center; 
            background-size: cover;
        """)

        # Контейнер для вопроса
        question_frame = QFrame()
        question_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(232, 213, 196, 180);
                border-radius: 15px;
                padding: 15px;
                border: 2px solid #9e7676;
            }
        """)
        question_layout = QVBoxLayout(question_frame)
        
        # Метка для вопроса
        self.question_label = QLabel()
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2d3436;
            margin-bottom: 10px;
            text-shadow: 1px 1px 2px #ffffff;
        """)
        self.question_label.setFont(QFont("Arial", 14, QFont.Bold))
        question_layout.addWidget(self.question_label)
        
        # Поле для отображения угаданных букв
        self.letters_frame = QFrame()
        self.letters_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(238, 214, 196, 100);
                border-radius: 10px;
                padding: 10px;
                border: 2px solid #9e7676;
            }
        """)
        self.letters_layout = QHBoxLayout(self.letters_frame)
        self.letters_layout.setAlignment(Qt.AlignCenter)
        self.letters_layout.setSpacing(10)
        
        question_layout.addWidget(self.letters_frame)
        game_layout.addWidget(question_frame)

        # Барабан
        self.wheel_label = QLabel()
        wheel_pixmap = QPixmap("wheel.jpg")
        self.wheel_pixmap = wheel_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.wheel_label.setPixmap(self.wheel_pixmap)
        self.wheel_label.setFixedSize(300, 300)
        self.wheel_label.setAlignment(Qt.AlignCenter)
        game_layout.addWidget(self.wheel_label, alignment=Qt.AlignCenter)

        # Счет
        self.score_label = QLabel(f"Очки: {self.total_score}")
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setStyleSheet("""
            font-size: 20px; 
            font-weight: bold; 
            color: #2d3436;
            margin-top: 10px;
            text-shadow: 1px 1px 2px #ffffff;
        """)
        game_layout.addWidget(self.score_label)

        # Кнопка вращения барабана
        self.spin_button = QPushButton("Вращать барабан")
        self.spin_button.setStyleSheet("""
            QPushButton {
                font-size: 18px; 
                padding: 12px; 
                border-radius: 10px; 
                background-color: #e8d5c4; 
                color: #2d3436;
                min-width: 200px;
                border: 2px solid #9e7676;
            }
            QPushButton:hover {
                background-color: #eed6c4;
                border-color: #815b5b;
            }
            QPushButton:disabled {
                background-color: rgba(232, 213, 196, 100);
                color: #95a5a6;
                border-color: #95a5a6;
            }
        """)
        self.spin_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.spin_button.clicked.connect(self.start_wheel_spin)
        game_layout.addWidget(self.spin_button, alignment=Qt.AlignCenter)

        # Поле ввода буквы
        self.input_field = QLineEdit()
        self.input_field.setMaxLength(1)
        self.input_field.setPlaceholderText("Введите букву")
        self.input_field.setStyleSheet("""
            QLineEdit {
                font-size: 18px; 
                padding: 10px; 
                border-radius: 10px; 
                background-color: #eed6c4;
                color: #2d3436;
                border: 2px solid #9e7676;
            }
            QLineEdit:disabled {
                background-color: rgba(238, 214, 196, 100);
                color: #95a5a6;
                border-color: #95a5a6;
            }
        """)

        # Кнопки действий
        button_style = """
            QPushButton {
                font-size: 16px; 
                padding: 10px; 
                border-radius: 10px; 
                background-color: #e8d5c4; 
                color: #2d3436;
                border: 2px solid #9e7676;
            }
            QPushButton:hover {
                background-color: #eed6c4;
                border-color: #815b5b;
            }
            QPushButton:disabled {
                background-color: rgba(232, 213, 196, 100);
                color: #95a5a6;
                border-color: #95a5a6;
            }
        """

        self.submit_button = QPushButton("Проверить букву")
        self.submit_button.setStyleSheet(button_style)
        self.submit_button.clicked.connect(self.check_letter)

        self.guess_word_button = QPushButton("Сказать слово")
        self.guess_word_button.setStyleSheet(button_style)
        self.guess_word_button.clicked.connect(self.guess_word)

        # Контейнер для ввода буквы и кнопок
        input_container = QHBoxLayout()
        input_container.setContentsMargins(50, 20, 50, 20)
        input_container.setSpacing(20)
        
        input_container.addWidget(self.input_field)
        input_container.addWidget(self.submit_button)
        input_container.addWidget(self.guess_word_button)

        game_layout.addLayout(input_container)

        # Метка для результатов
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold;
            color: #f39c12;
            margin-top: 10px;
        """)
        game_layout.addWidget(self.result_label)

        self.stacked_widget.addWidget(game_widget)

    def update_letters_display(self):
        """Обновляет отображение угаданных букв"""
        # Очищаем предыдущие буквы
        for i in reversed(range(self.letters_layout.count())): 
            self.letters_layout.itemAt(i).widget().setParent(None)
        
        # Добавляем новые буквы
        for letter in self.guessed_word:
            letter_label = QLabel(letter)
            letter_label.setAlignment(Qt.AlignCenter)
            letter_label.setStyleSheet("""
                font-size: 28px; 
                font-weight: bold; 
                color: #2d3436;
                background-color: #eed6c4;
                border-radius: 5px;
                min-width: 40px;
                min-height: 40px;
                padding: 5px;
                border: 2px solid #9e7676;
            """)
            letter_label.setFont(QFont("Arial", 18, QFont.Bold))
            self.letters_layout.addWidget(letter_label)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        # Выбираем случайное слово и вопрос
        self.current_word_data = random.choice(self.words_with_questions[difficulty])
        self.hidden_word = self.current_word_data["word"]
        self.guessed_word = ["_" for _ in self.hidden_word]
        
        # Устанавливаем вопрос
        self.question_label.setText(f"Вопрос: {self.current_word_data['question']}")
        
        # Обновляем отображение букв
        self.update_letters_display()
        
        self.total_score = 0
        self.current_spin_result = None
        self.current_potential_score = 0
        self.can_guess = False
        self.disable_input_controls()
        self.score_label.setText(f"Очки: {self.total_score}")
        self.stacked_widget.setCurrentIndex(1)

    def show_victory_dialog(self):
        dialog = VictoryDialog(self.total_score, self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            # Играть снова - возвращаемся к выбору сложности
            self.stacked_widget.setCurrentIndex(0)
            self.reset_game()
        else:
            # Выйти из игры
            QApplication.quit()

    def guess_word(self):
        if not self.can_guess:
            QMessageBox.warning(self, "Ошибка", "Сначала прокрутите барабан!")
            return

        while True:
            word, ok = QInputDialog.getText(
                self, 
                "Угадать слово", 
                "Введите полное слово:", 
                QLineEdit.Normal, 
                ""
            )
            
            if not ok:
                return

            if word and word.isalpha():
                break
            else:
                QMessageBox.warning(self, "Ошибка", "Слово должно состоять только из букв. Попробуйте еще раз.")
        
        if word.upper() == self.hidden_word:
            # Пользователь угадал слово
            self.guessed_word = list(self.hidden_word)
            self.update_letters_display()
            
            # Добавляем очки за текущий ход и бонус за угаданное слово
            bonus = len(self.hidden_word) * 300
            total_earned = self.current_potential_score + bonus
            self.total_score += total_earned
            self.score_label.setText(f"Очки: {self.total_score}")
            
            self.show_victory_dialog()
        else:
            QMessageBox.warning(
                self, 
                "Неверно", 
                "К сожалению, это не правильное слово. Очки не начисляются."
            )
            self.disable_input_controls()

    def check_letter(self):
        if not self.can_guess:
            QMessageBox.warning(self, "Ошибка", "Сначала прокрутите барабан!")
            return

        letter = self.input_field.text().upper()
        if not letter:
            QMessageBox.warning(self, "Ошибка", "Введите букву!")
            return

        if not letter.isalpha():
            QMessageBox.warning(self, "Ошибка", "Можно вводить только буквы.")
            self.input_field.clear()
            return

        found = False
        if letter in self.hidden_word:
            for i, char in enumerate(self.hidden_word):
                if char == letter:
                    self.guessed_word[i] = letter
                    found = True
            
            if found:
                self.total_score += self.current_potential_score
                self.update_letters_display()

                if "_" not in self.guessed_word:
                    self.show_victory_dialog()
                else:
                    QMessageBox.information(self, "Правильно!", f"Буква '{letter}' есть в слове! Вы получаете {self.current_potential_score} очков!")
            else:
                QMessageBox.warning(self, "Неверно", "Вы не угадали букву. Очки не начисляются.")
        else:
            QMessageBox.warning(self, "Неверно", "Такой буквы нет в слове. Очки не начисляются.")

        self.input_field.clear()
        self.disable_input_controls()
        self.score_label.setText(f"Очки: {self.total_score}")

    def start_wheel_spin(self):
        self.spin_angle = 0
        self.spin_button.setEnabled(False)
        self.result_label.setText("")
        self.spin_timer.start(50)

    def update_wheel_rotation(self):
        self.spin_angle += 30
        transform = QTransform().rotate(self.spin_angle % 360)
        rotated_pixmap = self.wheel_pixmap.transformed(transform, Qt.SmoothTransformation)
        self.wheel_label.setPixmap(rotated_pixmap)

        if self.spin_angle >= 360 * random.randint(2, 4):
            self.spin_timer.stop()
            self.spin_button.setEnabled(True)
            self.finalize_spin()

    def finalize_spin(self):
        self.current_spin_result = random.choice(self.sectors[self.difficulty])
        self.result_label.setText(f"Выпало: {self.current_spin_result}")

        if self.current_spin_result == "Банкрот":
            self.total_score = 0
            self.can_guess = False
            QMessageBox.warning(self, "Банкрот", "Вы потеряли все очки!")
            self.disable_input_controls()
        elif self.current_spin_result == "Приз":
            self.current_potential_score = random.randint(100, 500)
            self.can_guess = True
            self.enable_input_controls()
        else:
            self.current_potential_score = int(self.current_spin_result.strip("+"))
            self.can_guess = True
            self.enable_input_controls()

        self.score_label.setText(f"Очки: {self.total_score}")

    def enable_input_controls(self):
        self.input_field.setEnabled(True)
        self.submit_button.setEnabled(True)
        self.guess_word_button.setEnabled(True)
        self.spin_button.setEnabled(False)

    def disable_input_controls(self):
        self.input_field.setEnabled(False)
        self.submit_button.setEnabled(False)
        self.guess_word_button.setEnabled(False)
        self.spin_button.setEnabled(True)
        self.current_spin_result = None
        self.current_potential_score = 0

    def reset_game(self):
        self.stacked_widget.setCurrentIndex(0)
        self.current_word_data = None
        self.hidden_word = ""
        self.guessed_word = []
        self.total_score = 0
        self.current_spin_result = None
        self.current_potential_score = 0
        self.can_guess = False
        self.disable_input_controls()
        self.score_label.setText(f"Очки: {self.total_score}")
        self.update_letters_display()

if __name__ == "__main__":
    app = QApplication([])
    window = PoleChudesGame()
    window.show()
    app.exec_()
