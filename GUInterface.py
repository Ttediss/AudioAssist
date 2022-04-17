from asyncio.windows_events import NULL
import PySimpleGUI as sg


class AmurGUI:

    def __init__(self):

        layout = [
            [sg.Output(size=(60, 15), key='-out_text-'),
            sg.Image(r'example.png',size=(300,212),key='-img_code-')],
            [sg.Button('Старт', key='-bt_start-',size=(6, 2)),
             sg.Button('Стоп', key='-bt_stop-',size=(6, 2)),
             sg.Button('Тест', key='-bt_test-',size=(6, 2))]
        ]
        self.out_texts =''
        self.window = sg.Window('AudioAssist', layout, size=(800, 450))


    def window_event(self):
        while True:
            event, value = self.window.read()
            yield event, value


    def window_handler(self):
        # while True:
        for event, value in self.window_event():
            # event, value = self.window.read()
            if event == '-bt_start-':
                self.Print('уже старт')
            elif event == '-bt_stop-':
                break
            elif event == '-bt_test-':
                self.Print('я не знаю, что делать')
            elif event == sg.WIN_CLOSED:    
                break

    def Print(self,text):
        text_output_elem = self.window['-out_text-']
        self.out_texts=self.out_texts +'\n'+text
        text_output_elem.update(self.out_texts)


if __name__ == "__main__":
    gui = AmurGUI()

    gui.window_handler()
    gui.window.close()