from contextlib import nullcontext
import json

import datetime

import pyaudio
from vosk import Model, KaldiRecognizer

import sys
import threading
import logging
import text_reproduction as tr
from GUI import Ui_MainWindow
from PyQt5 import QtWidgets
# модуль стз----------------------------
import numpy as np
import cv2
import cv2.aruco as aruco
# from cv2 import aruco as aruco
import math
import time
from PyQt5 import QtGui
import qimage2ndarray
from PyQt5.QtGui import QImage
# --------------------------------------

class VoiceAssistant:
    # private
    __ttsEngine = nullcontext
    __rec = nullcontext
    __stream = nullcontext

    # setup_assistant_voices
    def __init__(self):
        model = Model("osk-model-small-ru-0.4")
        self.__rec = KaldiRecognizer(model, 16000)
        p = pyaudio.PyAudio()
        self.__stream = p.open(format=pyaudio.paInt16, channels=1,
                        rate=16000, input=True, frames_per_buffer=8000)
        self.__stream.start_stream()


    def listen(self):
        while True:

            data = self.__stream.read(4000, exception_on_overflow=False)
            if (self.__rec.AcceptWaveform(data)) and (len(data) > 0):
                answer = json.loads(self.__rec.Result())
                if answer['text']:
                    yield answer['text']

# разобрать---------------------------------------------
class MainV(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.action()
        self.flag_a = 0
        self.flag_v = 0
        # Приветствие------------------------------------------------------------
        hello = " Приветствую вас!"
        working = " Работаем!"

        logger.info(hello)
        tr.voice_acting.say(" Приветствую вас!")
        logger.info(working)
        tr.voice_acting.say(working)

    # --------------------------------------------------------------

    def action(self):
        self.btn_start.clicked.connect(self.start)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_screenshot.clicked.connect(self.savePhoto)

    def savePhoto(self):
        self.image = self.img
        self.filename = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        try:
            self.image.save(self.filename, "PNG")
            print('Изобаржение сохранено как:', self.filename)
            dt = str(datetime.datetime.now())
            mainV.textBrowser.append(dt + " Изобаржение сохранено как:" + self.filename)
            logger.info("Изобаржение сохранено как:" + self.filename)
        except:
            print(str(time.strftime("%Y-%b-%d at %H.%M.%S %p"))+"Снимок не удался")

    #
    # def brightness_value(self, value):
    #
    #     self.brightness_value_now = value
    #     #print('Brightness: ', value)
    #     self.update()
    #
    # def update(self):
    #     img = self.changeBrightness(self.image, self.brightness_value_now)
    #
    # def changeBrightness(self, img, value):
    #     """ This function will take an image (img) and the brightness
    #         value. It will perform the brightness change using OpenCv
    #         and after split, will merge the img and return it.
    #     """
    #     hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     h, s, v = cv2.split(hsv)
    #     lim = 255 - value
    #     v[v > lim] = 255
    #     v[v <= lim] += value
    #     final_hsv = cv2.merge((h, s, v))
    #     img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    #     return img
    #
    def start(self):
        logger.info("Нажатие кнопки \"Старт\"")
        if mainV.checkBox_voice.isChecked():
            self.t_audio = threading.Thread(target=self.audio, name='t_audio')
            self.t_audio.start()
            self.flag_a = 1
            mainV.textBrowser.append("Голосовой помошник включен")
            logger.info("Голосовой помошник включен")
        else:
            mainV.textBrowser.append("Голосовой помошник не включен")
            logger.info("Голосовой помошник не включен")
        if mainV.checkBox_video.isChecked():
            self.t_video = threading.Thread(target=self.Video, name='t_video')
            self.t_video.start()
            self.flag_v = 1
            mainV.textBrowser.append("СТЗ включена")
            logger.info("СТЗ включена")
        else:
            mainV.textBrowser.append("СТЗ не включена")
            logger.info("СТЗ не включена")


    def audio(self):

        print("Start audio")
        while True:
            if self.flag_a == 1:
                if mainV.checkBox_voice.isChecked():
                    dt = str(datetime.datetime.now())
                    mainV.textBrowser.append(dt)
                    mainV.textBrowser.append("Эксперимент: " + mainV.exp_name.text() )
                    logger.info("Эксперимент: " + mainV.exp_name.text())
                    # настройки озвучки ----------------------------------------------------------------------
                    if mainV.voice_rate.text()!="":
                        tr.voice_acting.settings('rate', int(mainV.voice_rate.text()))
                        mainV.textBrowser.append("Скорость речи: " + mainV.voice_rate.text())
                        logger.info("Скорость речи: " + mainV.voice_rate.text())
                    else:
                        tr.voice_acting.settings('rate', 180)
                        mainV.textBrowser.append("Скорость речи: 180" )
                        logger.info("Скорость речи: 180" )
                    if mainV.voice_volume.text()!="":
                        tr.voice_acting.settings('volume', float(mainV.voice_volume.text()))
                        mainV.textBrowser.append("Громость речи: " + mainV.voice_volume.text())
                        logger.info("Громость речи: " + mainV.voice_volume.text())
                    else:
                        tr.voice_acting.settings('volume', 0.9)
                        mainV.textBrowser.append("Громость речи: 0.9" )
                        logger.info("Громость речи: 0.9")
                    # ---------------------------------------------------------------------------------------

                    # listen_handler()
                    for text in assistant.listen():

                        if self.flag_a == 1:

                            # tr.voice_acting.say(text)
                            logger.info(text)
                            dt = str(datetime.datetime.now())
                            if "амур триста семь" in text or "амур" in text:
                                mainV.textBrowser.append(dt + " " + text)

                                if "привет" in text:
                                    answer = " АМУР: приветствую вас, сэр!"
                                    mainV.textBrowser.append(dt + answer)
                                    logger.info(answer)
                                    tr.voice_acting.say("приветствую вас, сэр!")
                                    text = ""

                                elif "состояние" in text:
                                    answer = " АМУР: я нахожусь в стадии разработки"
                                    mainV.textBrowser.append(dt + answer)
                                    logger.info(answer)
                                    tr.voice_acting.say("я нахожусь в стадии разработки")
                                    text = ""
                                elif "отбой" in text:
                                    answer = ' АМУР: всего доброго сэр!'
                                    mainV.textBrowser.append(dt + answer)
                                    logger.info(answer)
                                    tr.voice_acting.say("всего доброго сэр!")
                                    text = ""
                                    sys.exit()
                                else:
                                    answer = " АМУР: я не понимаю вас"
                                    mainV.textBrowser.append(dt + answer)
                                    logger.info(answer)
                                    tr.voice_acting.say("я не понимаю вас")
                                    text = ""
                else:
                    mainV.textBrowser.append("Голосовой помошник не включен")
                    logger.info("Голосовой помошник не включен")
                    break

            else:

                break
    def Video(self):

        print("Start video")
        tr.voice_acting.say("видео грузится")
        dt = str(datetime.datetime.now())
        mainV.textBrowser.append(dt+"Видео грузится")
        logger.info("Видео грузится")
        while True:
            if self.flag_v == 1:
                if mainV.checkBox_video.isChecked(): # СТЗ---------------------------------------------------

                    dt = str(datetime.datetime.now())
                    # настройки изображения ----------------------------------------------------------------------
                    if mainV.marker_size.text() != "": # Размер маркера
                        Scale = mainV.marker_size.text()
                        mainV.textBrowser.append("Размер маркера: " + mainV.marker_size.text() + " м")
                        logger.info("Размер маркера: " + mainV.marker_size.text())
                    else:
                        Scale = 0.05
                        mainV.textBrowser.append("Размер маркера выбран по умолчанию: 0.05 м")
                        logger.info("Размер маркера выбран по умолчанию: 0.05 м")
#?                    t = 0  # Время начала
                    # Выбор словаря маркеров. В нашем случае выбран словарь с маркерами 5*5 ячеек содержащий 1000 различных маркеров
                    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
                    mainV.textBrowser.append("Используется словарь с маркерами 5*5 ячеек, содержащий 1000 различных маркеров")
                    logger.info("Используется словарь с маркерами 5*5 ячеек, содержащий 1000 различных маркеров")
                    # Создаем массив с параметрами определения маркеров
                    parameters = aruco.DetectorParameters_create()
                    logger.info("Создан массив с параметрами определения маркеров")
                    # Записываем матрицу камеры.
                    if mainV.camera_matrix.text() != "":
                        mtx = np.array(mainV.camera_matrix.text())
                        mainV.textBrowser.append("Матрица камеры задана: " + mainV.camera_matrix.text() )
                        logger.info("Матрица камеры задана: " + mainV.camera_matrix.text())
                    else:
                        mtx = np.array([[936.358, 0., 765.965], [0., 965.580, 400.186], [0., 0., 1.]])
                        mainV.textBrowser.append("Матрица камеры выбрана по умолчанию: [[936.358, 0., 765.965], [0., 965.580, 400.186], [0., 0., 1.]]")
                        logger.info("Матрица камеры выбрана по умолчанию: [[936.358, 0., 765.965], [0., 965.580, 400.186], [0., 0., 1.]]")

                    # Задаем матрицу дисторсии камеры. обе матрицы были получены с помощью калибровки
                    if mainV.cam_distortion_matrix.text() != "":
                        distor = np.array(mainV.cam_distortion_matrix.text())
                        mainV.textBrowser.append("Размер маркера: " + mainV.cam_distortion_matrix.text() )
                        logger.info("Размер маркера: " + mainV.cam_distortion_matrix.text())
                    else:
                        distor = np.array([0.141793, -0.152794, -0.023574, 0.026615])
                        mainV.textBrowser.append("Матрица дисторсии камеры выбрана по умолчанию: [0.141793, -0.152794, -0.023574, 0.026615]")
                        logger.info("Матрица дисторсии камеры выбрана по умолчанию: [0.141793, -0.152794, -0.023574, 0.026615]")

                    # создаем объект cap для захвата кадров с камеры
                    if mainV.index_camera.text() != "":
                        cap = cv2.VideoCapture(int(mainV.index_camera.text()))
                        mainV.textBrowser.append("Индекс камеры: " + mainV.index_camera.text() )
                        logger.info("Индекс камеры: " + mainV.index_camera.text())
                    else:
                        cap = cv2.VideoCapture(0)
                        mainV.textBrowser.append("Индекс камеры по умолчанию: 0")
                        logger.info("Индекс камеры по умолчанию: 0")

                    if mainV.frame_rate.text() != "":
                        cap.set(cv2.CAP_PROP_FPS, int(mainV.frame_rate.text()))
                        mainV.textBrowser.append("Частота кадров: " + mainV.frame_rate.text() )
                        logger.info("Частота кадров: " + mainV.frame_rate.text())
                    else:
                        cap.set(cv2.CAP_PROP_FPS, 24)  # Частота кадров
                        mainV.textBrowser.append("Частота кадров: 24")
                        logger.info("Частота кадров: 24" )
                    if mainV.frame_rate.text() != "":
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(mainV.frame_w.text()))
                        mainV.textBrowser.append("Ширина кадров: " + mainV.frame_w.text() )
                        logger.info("Ширина кадров: " + mainV.frame_w.text())
                    else:
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)  # Ширина кадров в видеопотоке.
                        mainV.textBrowser.append("Ширина кадров: 600")
                        logger.info("Ширина кадров: 1280")

                    if mainV.frame_rate.text() != "":
                        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(mainV.frame_h.text()))
                        mainV.textBrowser.append("Высота кадров: " + mainV.frame_h.text())
                        logger.info("Высота кадров: " + mainV.frame_h.text())
                    else:
                        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)  # Высота кадров в видеопотоке.
                        mainV.textBrowser.append("Высота кадров: 400")
                        logger.info("Высота кадров: 720")
                    tr.voice_acting.say("видео пошло")
                    mainV.textBrowser.append(dt + "Видео пошло")
                    logger.info("Видео пошло")
                    cvNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'graph.pbtxt')
                    while True:
                        QtWidgets.QApplication.processEvents()
                        # захватываем текущий кадр и кладем его в переменную img
                        flag, self.img = cap.read()
                        # mainV.video = imutils.resize(img, height= 720)
                        # Определяем аруко-маркеры на кадре
                        corners, ids, rejectedImgPoints = aruco.detectMarkers(
                            self.img, aruco_dict, parameters=parameters)


                        rows = self.img.shape[0]
                        cols = self.img.shape[1]
                        cvNet.setInput(cv2.dnn.blobFromImage(self.img, size=(300, 300), swapRB=True, crop=False))
                        cvOut = cvNet.forward()
                        for detection in cvOut[0, 0, :, :]:
                            score = float(detection[2])
                            if score > 0.3:
                                left = detection[3] * cols
                                top = detection[4] * rows
                                right = detection[5] * cols
                                bottom = detection[6] * rows
                                #print("--- %s seconds ---" % (time.time() - last_time))
                                last_time = time.time()
                                cv2.rectangle(self.img, (int(left), int(top)), (int(right), int(bottom)), (23, 230, 210),
                                              thickness=2)

                        # Если маркеры были определены то запускаем следующий цикл
                        if ids is not None:
                            # Замеряем время начала
                            start = time.time()
                            print(corners, ids, rejectedImgPoints)
                            # Выделяем зеленой рамкой обнаруженные маркеры на кадре
                            aruco.drawDetectedMarkers(self.img, corners, ids)
                            # Выделяем красной рамкой отброшенные попытки определить
                            aruco.drawDetectedMarkers(self.img, rejectedImgPoints, borderColor=(100, 0, 240))
                            # Определяем положение маркеров относительно камеры
                            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corners, Scale, mtx, distor)
                            # rvec = np.array([[[0.0, 0.0, 0.0]]])
                            # Для каждого маркера в кадре проводим следующее
                            for i in range(0, ids.size):
                                # Записываем вектор поворота из массива в отдельную переменную
                                rvecs = rvec[i]
                                # Записываем вектор перемещения из массива в отдельную переменную
                                tvecs = tvec[i]
                                # Строим оси на изображении для каждого маркера
                                aruco.drawAxis(self.img, mtx, distor, rvecs, tvecs, 0.5 * Scale)
                                # С помощью формулы Родрига переводим вектор поворота в матрицу поворота и матрицу Якоби
                                RotMat, Jac = cv2.Rodrigues(rvecs[0])
                                # Транспонируем вектор перемещений
                                tvecsTr = np.array([[tvecs[0][0]], [tvecs[0][1]], [tvecs[0][2]]])
                                # Перемножаем матрицу поворота с вектором перемещений для получения координат маркера
                                Trans = RotMat.dot(tvecsTr)
                                # Высчитываем расстояния от камеры до маркера
                                Trans1 = math.sqrt((Trans[0][0] ** 2) + (Trans[1][0] ** 2) + (Trans[2][0] ** 2))
                                # Вывод полученной информации в консоль
                                print("матрица поворота", ids[i][0], ":", RotMat, "вектор перемещения", ids[i][0], ":",
                                      tvecs,
                                      "вектор поворота", ids[i][0], ":", rvecs, "вектор координат", ids[i][0], ":",
                                      Trans)
                                # Отображаем в окне синим цветом расстояние от маркера до камеры
                                cv2.putText(self.img, "Dist %.4f mm -- ID %.3f " % ((Trans1 * 1000), (ids[i][0])),
                                            (0, 100 + i * 50),
                                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (244, 0, 144))
                            # Замеряем время после обработки всех маркеров и вычисляем время выполнения цикла обработки
                            # end = time.time()
                            # t = end - start
                        try:
                            # отображаем кадр в окне с именем result

                            self.img = qimage2ndarray.array2qimage(self.img)  # pip install qimage2ndarray
                            mainV.video.setPixmap(QtGui.QPixmap.fromImage(self.img))

                            # Выводим время выполнения в консоль
                            # print("time", t)
                        except:
                            cap.release()
                            raise
                        # Закрываем окно и завершаем работу программы при нажатии ESC
                        ch = cv2.waitKey(10)
                        if ch == 27:
                            break

                        if self.flag_v == 0:
                            break
                    cap.release()
                    cv2.destroyAllWindows()

                    # ---------------------------------------------------------------------------------------
                    continue

                else:
                    mainV.textBrowser.append("СТЗ отключена")
                    logger.info("СТЗ отключена")
                    break
            else:
                break


    def stop(self):
        self.flag_a = 0
        self.flag_v = 0
        mainV.textBrowser.append("Stop\n")
        logger.info("Нажатие кнопки \"Стоп\"")
        dt = str(datetime.datetime.now())
        print(dt+'Стоп')
# ---------------------------------------------------------



# def listen_handler():
#
#     for text in assistant.listen():
#         tr.voice_acting.say(text)
#         logger.info(text)
#         if "амур триста семь" in text or "амур" in text:
#             dt = str(datetime.datetime.now())
#             mainV.textBrowser.append(dt + " " + text)
#             if "привет" in text:
#                 answer = " АМУР: приветствую вас, сэр!\n"
#                 mainV.textBrowser.append(dt + answer)
#                 logger.info(answer)
#                 tr.voice_acting.say("приветствую вас, сэр!")
#                 text = ""
#
#             elif "состояние" in text:
#                 answer = " АМУР: я нахожусь в стадии разработки\n"
#                 mainV.textBrowser.append(dt + answer)
#                 logger.info(answer)
#                 tr.voice_acting.say("я нахожусь в стадии разработки")
#                 text = ""
#             elif "отбой" in text:
#                 answer = ' АМУР: всего доброго сэр!\n'
#                 mainV.textBrowser.append(dt + answer)
#                 logger.info(answer)
#                 tr.voice_acting.say("всего доброго сэр!")
#                 text = ""
#                 sys.exit()
#             else:
#                 answer = " АМУР: я не понимаю вас\n"
#                 mainV.textBrowser.append(dt + answer)
#                 logger.info(answer)
#                 tr.voice_acting.say("я не понимаю вас")
#                 text = ""






if __name__ == "__main__":
    assistant = VoiceAssistant()
    #gui = AmurGUI()

    # настройки озвучки по умолчанию-------------------------------------------------------------------
    tr.voice_acting.settings('rate', 180)
    tr.voice_acting.settings('volume', 0.9)
    #---------------------------------------------------------------------------------------

    # настроки камеры по умолчанию------------------------------------------------------------
    Scale = 0.05 #Размер маркера
    t=0           #Время начала
    #Выбор словаря маркеров. В нашем случае выбран словарь с маркерами 5*5 ячеек содержащий 1000 различных маркеров
    aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_1000)
    #Создаем массив с параметрами определения маркеров
    parameters = aruco.DetectorParameters_create()
    #Записываем матрицу камеры.
    mtx = np.array([[936.358,  0. , 765.965], [0.,  965.580,  400.186], [0., 0., 1.]])
    #Задаем матрицу дисторсии камеры. обе матрицы были получены с помощью калибровки
    distor = np.array([0.141793,  -0.152794,  -0.023574,  0.026615])
    #---------------------------------------------------------------------------------------

    # новое логирование ----------------------------------------------------------------------
        # Создание экземпляра логера
    logger = logging.getLogger("main")
    logger.setLevel(logging.INFO)
        # Создание обработчика лог файла
    LOG = logging.FileHandler('log.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s','%Y-%m-%d %H:%M:%S')
    LOG.setFormatter(formatter)
     # добавляем обработчик к объекту логгера
    logger.addHandler(LOG)
    logger.info("Program started")
    #----------------------------------------------------------------------


    # Новый интерфейс-----------------------

    app = QtWidgets.QApplication(sys.argv)
    mainV = MainV()
    mainV.show()
    sys.exit(app.exec_())
    # ----------------------

    # test
    #test
