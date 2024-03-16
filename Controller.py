import os
from Model import Model
from View import View
from tkinter import filedialog as fd
class Controller:
    def __init__(self):
        self.__model = Model()
        self.__view = View(self, self.__model)

    def main(self):
        self.__view.main()

    def open_file(self):
        filetypes = (
            ('CSV files', '*.csv'),
        )
        filepath = fd.askopenfilename(filetypes=filetypes)
        if filepath:
            filename = os.path.basename(filepath)
            self.__view.clear(0, '')
            self.__view.insert['state'] = 'normal'
            self.__view.btn_search['state'] = 'normal'
            self.__view.lbl_filename['text'] = filename
            self.__model.filename = filepath

    def search_value(self):
        insert = self.__view.insert.get().strip()
        if len(insert) >= 3:
            header, data = self.__model.read_data()
            search_data = self.__model.search_data(insert, data)
            count = len(search_data)
            if count > 0:
                self.__view.insert.delete(0, 'end')
                self.__view.error_lbl['text'] = ''
                self.__view.lbl_count['text'] = count
                self.__view.lbl_entry_insert['text'] = 'Otsingusõna: ' + insert
                self.__view.clear_insert()
                self.__view.draw_search_result(header, search_data)

            else:
                self.__view.clear(0, 'Otsingusõnale ei olnud vastet')
        else:
            self.__view.clear(0, 'Palun sisesta 3 või rohkem märki')

    # Antud funktsioon ei sule file-i, kuid tühjendab muud väljad ja muudab Otsi nupu ja entry disabled staatusesse.
    # Pole muud võimalust kui avada uuesti .csv, et jätkata ning seda tahes taastub algne seis
    def clear_all_fields(self):
        self.__view.lbl_entry_insert['text'] = 'Sisestatud otsingusõna'
        self.__view.clear_insert()
        self.__view.lbl_filename['text'] = 'Fail pole valitud'
        self.__view.lbl_count['text'] = 0
        self.__view.insert.config(state='disabled')
        self.__view.btn_search.config(state='disabled')
        # self.__model.close_file(self) # Ei saanud file-i suletus
