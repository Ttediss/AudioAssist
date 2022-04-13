from asyncio.windows_events import NULL
import PySimpleGUI as sg


class AmurGUI:

    def __init__(self):
        layout = [
            [sg.Output(size=(200, 15), key='-out_text-')],
            [sg.Button('Старт', key='-bt_start-'),
             sg.Button('Стоп', key='-bt_stop-')]
        ]
        self.out_texts =''
        self.window = sg.Window('AudioAssist', layout, size=(600, 350))


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