import PySimpleGUI as sg

# def window():
#     layout = [
#         [sg.Output(size=(20, 15))],
#         [sg.Button('Старт'), sg.Button('Стоп')]
#         ]
#     sg.Window('AudioAssist').Layout(layout)

def Print(text):
    layout = [
                [sg.Output(size=(20, 15))],
                [sg.Button('Старт'), sg.Button('Стоп')]
                ]
    sg.Window('AudioAssist').Layout(layout)
    sg.Print(text)