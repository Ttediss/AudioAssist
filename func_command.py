import datetime

class Parameters:
    Gus_forward = 0  # глобальная переменная, отвечающая за хранения данных о перемещении гусеницы вперед
    Gus_back = 0  # глобальная переменная, отвечающая за хранения данных о перемещении гусеницы назад
    Gus_right = 0  # глобальная переменная, отвечающая за хранения данных о перемещении гусеницы направо
    Gus_left = 0  # глобальная переменная, отвечающая за хранения данных о перемещении гусеницы налево
    Manipulator_up = 0  # глобальная переменная, отвечающая за хранения данных о подъеме манипулятор
    Manipulator_down = 0  # глобальная переменная, отвечающая за хранения данных об опускании манипулятора
    Manipulator_flag = 0  # глобальная переменная, отвечающая за состояние манипулятора
    Camera_right = 0  # глобальная переменная, отвечающая за хранения данных о перемещении камеры направо
    Camera_left = 0  # глобальная переменная, отвечающая за хранения данных о перемещении камеры налево

logs = 'logs.txt'  # имя и расширение файла (лога)
voice_command = ' '  # запись голосовой команды (для лога)
# Класс гусениц
class Caterpillars:
    @staticmethod
    def forward_back(voice, move):  # Метод отвечает за команды вперёд/назад
        global voice_command
        voice_split = str(voice).replace(",", ".").split(' ')
        voice_replace = str(voice_split[2]).replace("м", "")

        if move:  # при значении True вперёд
            Parameters.Gus_forward = float(voice_replace)
            voice_command = "вперёд на " + str(Parameters.Gus_forward)
            print(Parameters.Gus_forward)
        elif not move:  # при значение False назад
            Parameters.Gus_back = float(voice_replace)
            voice_command = "назад на " + str(Parameters.Gus_back)
            print(Parameters.Gus_back)

        with open(logs, 'a') as s_file:  # запись в логи
            s_file.write(str(datetime.datetime.now()) + ": Гусеницы || " + voice_command + " м" + "\n")

    @staticmethod
    def right_left(voice, rotation):  # Метод отвечает за команды направо/налево
        global voice_command
        voice_split = str(voice).split(' ')

        if (voice_split[3]) == "один":
            voice_split[3] = 1

        if rotation:  # при значении True поворот направо
            Parameters.Gus_right = int(voice_split[3])
            voice_command = "поворот направо на " + str(Parameters.Gus_right)
            print(Parameters.Gus_right)
        elif not rotation:  # при значении False поворот налево
            Parameters.Gus_left = int(voice_split[3])
            voice_command = "поворот налево на " + str(Parameters.Gus_left)
            print(Parameters.Gus_left)

        with open(logs, 'a') as s_file:  # запись в логи
            s_file.write(str(datetime.datetime.now()) + ": Гусеницы || " + voice_command + " град" + "\n")

    @staticmethod
    def caterpillars(voice):  # финальный метод (условия)
        voice_split = str(voice).split(' ')
        if voice_split[0] == "вперёд":
            Caterpillars.forward_back(voice, True)  # при значении True движение вперед

        elif voice_split[0] == "назад":
            Caterpillars.forward_back(voice, False)  # при значении False движение назад

        elif (voice_split[0] + ' ' + voice_split[1]) == "поворот направо":
            Caterpillars.right_left(voice, True)  # при значении True поворот направо

        elif (voice_split[0] + ' ' + voice_split[1]) == "поворот налево":
            Caterpillars.right_left(voice, False)  # при значении False поворот налево

    # Класс манипулятора
class Manipulator:
    @staticmethod
    def up_down(voice, position):  # Метод отвечает за команды манипулятора вверх/вниз
        global voice_command
        voice_split = str(voice).replace(",", ".").split(' ')
        voice_replace = str(voice_split[3]).replace("см", "")

        if (voice_split[3]) == "один":
            voice_split[3] = 1

        if position:  # при значении True манипулятор движется вверх
            Parameters.Manipulator_up = float(voice_replace)
            voice_command = "поднять на " + str(Parameters.Manipulator_up)
            print(Parameters.Manipulator_up)
        elif not position:  # при значении False манипулятор движется вниз
            Parameters.Manipulator_down = float(voice_replace)
            voice_command = "опустить на " + str(Parameters.Manipulator_down)
            print(Parameters.Manipulator_down)

        with open(logs, 'a') as s_file:  # запись в логи
            s_file.write(str(datetime.datetime.now()) + ": Манипулятор || " + voice_command + " см" + "\n")

    @staticmethod
    def flag(flag):  # Метод отвечает за команды манипулятора схватить/отпустить
        global voice_command
        if flag:
            Parameters.Manipulator_flag = True
            voice_command = "состояние схвата: " + str(Parameters.Manipulator_flag)
            print(Parameters.Manipulator_flag)
        elif not flag:
            Parameters.Manipulator_flag = False
            voice_command = "состояние схвата: " + str(Parameters.Manipulator_flag)
            print(Parameters.Manipulator_flag)

        with open(logs, 'a') as s_file:  # запись в логи
            s_file.write(str(datetime.datetime.now()) + ": Манипулятор || " + voice_command + "\n")

    @staticmethod
    def manipulator(voice):  # финальный метод (условия)
        voice_split = str(voice).split(' ')
        if (voice_split[0] + ' ' + voice_split[1]) == "поднять манипулятор":
            Manipulator.up_down(voice, True)
        elif (voice_split[0] + ' ' + voice_split[1]) == "опустить манипулятор":
            Manipulator.up_down(voice, False)

        # схват манипулятора
        elif (voice_split[0] + ' ' + voice_split[1]) == "схватить объект" or (voice_split[0] + ' ' + voice_split[1]) == "захватить объект":
            Manipulator.flag(True)
        elif (voice_split[0] + ' ' + voice_split[1]) == "отпустить объект":
            Manipulator.flag(False)

# Класс камеры
class Camera:
    @staticmethod
    def right_left(voice, rotation):  # Метод отвечает за команды камеры направо/налево
        global voice_command
        voice_split = str(voice).split(' ')
        if voice_split[3] == "один" or voice_split[4] == "один":
            voice_split[3] = 1
            voice_split[4] = 1

        if rotation:
            try:
                Parameters.Camera_right = int(voice_split[4])
                print(Parameters.Camera_right)
            except ValueError:
                Parameters.Camera_right = int(voice_split[3])
                print(Parameters.Camera_right)
            voice_command = "направа на " + str(Parameters.Camera_right)

        elif not rotation:
            try:
                Parameters.Camera_left = int(voice_split[4])
                print(Parameters.Camera_left)
            except ValueError:
                Parameters.Camera_left = int(voice_split[3])
                print(Parameters.Camera_left)
            voice_command = "налево на " + str(Parameters.Camera_left)

            with open(logs, 'a') as s_file:  # запись в логи
                s_file.write(str(datetime.datetime.now()) + ": Камера || " + voice_command + " град" + "\n")

    @staticmethod
    def camera(voice):  # Финальный метод (условия)
        voice_split = str(voice).split(' ')
        if voice_split[0] == "камера" or voice_split[0] == "камеры":
            if voice_split[1] == "направо" or (voice_split[1] + ' ' + voice_split[2]) == "на права" \
                    or (voice_split[1] + ' ' + voice_split[2]) == "на право" or voice_split[1] == "направлена":
                Camera.right_left(voice, True)
            elif voice_split[1] == "налево" or (voice_split[1] + ' ' + voice_split[2]) == "на лево":
                Camera.right_left(voice, False)

# Класс данных
class Date:
    @staticmethod
    def date(voice):  # Выводит значения всех переменных
        voice_split = str(voice).split(' ')
        if (voice_split[0] + ' ' + voice_split[1]) == "данные переменных" \
                or (voice_split[0] + ' ' + voice_split[1]) == "данный переменных":
            print("\nПеремещение гусеницы:\nВперёд " + str(Parameters.Gus_forward) + " м\nНазад "
                  + str(Parameters.Gus_back) + " м\nПоворот направо " + str(Parameters.Gus_right)
                  + " град\nПоворот налево " + str(Parameters.Gus_left) + " град\n\nМанипулятор:\nВверх "
                  + str(Parameters.Manipulator_up) + " см\nВниз " + str(Parameters.Manipulator_down)
                  + " см\nСостояние схвата: " + str(Parameters.Manipulator_flag) + "\n\nКамера:\nНаправо "
                  + str(Parameters.Camera_right) + " град\nНалево " + str(
                Parameters.Camera_left) + " град\n")
