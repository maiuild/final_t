from tkinter import *
from tkinter import ttk
import tkinter.font as font


class View(Tk):
    def __init__(self, controller, model):
        super().__init__()
        self.__controller = controller
        self.__model = model

        self.__width = 650
        self.__height = 500
        self.__default = font.Font(family='Verdana', size=14)

        self.title("Otsingu rakendus")

        self.center(self, self.__width, self.__height)

        # Frame'ide loomine loomine
        self.top_frame = self.create_top_frame()
        self.bottom_frame = self.create_bottom_frame()
        self.third_frame = self.create_third_frame()

        # Labelite loomine
        (self.__lbl_form, self.__open_file_lbl, self.__filename_lbl, self.__lbl_entry_insert,
         self.__row_count_lbl, self.__count_lbl, self.__error_lbl) = self.create_labels()

        # Entry
        self.__insert = Entry(self.top_frame, font=self.__default)
        self.__insert['state'] = 'disabled'
        self.__insert.grid(row=0, column=2, padx=5, pady=2, sticky=EW)

        # Nuppude loomine
        self.__btn_search, self.__btn_ope, clear_btn = self.create_buttons()

        self.bind('<Return>', lambda event: self.__controller.search_value())

    @property
    def insert(self):
        return self.__insert

    @property
    def lbl_filename(self):
        return self.__filename_lbl

    @property
    def lbl_count(self):
        return self.__count_lbl

    @property
    def btn_search(self):
        return self.__btn_search

    @property
    def error_lbl(self):
        return self.__error_lbl
    @property
    def lbl_entry_insert(self):
        return self.__lbl_entry_insert

    def main(self):
        self.mainloop()

    @staticmethod
    def center(win, w, h):
        x = int((win.winfo_screenwidth() / 2) - (w / 2))
        y = int((win.winfo_screenheight() / 2) - (h / 2))
        win.geometry(f'{w}x{h}+{x}+{y}')

    def create_top_frame(self):
        frame = Frame(self, bg='lightblue', height=15)
        frame.pack(fill=BOTH)  # BOTH on tkinteris konstant
        return frame  # tagastame frame´i et saaks seda mujal kasutada

    def create_bottom_frame(self):
        frame = Frame(self, bg='azure1')
        frame.pack(expand=True, fill=BOTH)
        return frame

    def create_third_frame(self):
        frame = Frame(self, bg='lightblue')
        frame.pack(expand=NO, fill=BOTH)
        return frame

    def create_buttons(self):
        btn_search = Button(self.top_frame, text='3. Otsi failist', font=self.__default, state='disabled',
                        command=self.__controller.search_value)
        btn_search.grid(row=1, column=2, padx=5, pady=5, sticky=EW)
        open_btn = Button(self.top_frame, text='1. Ava fail', font=self.__default, command=self.__controller.open_file)
        open_btn.grid(row=0, column=0, padx=5, pady=5, sticky=EW)

        clear_btn = Button(self.top_frame, text='* Puhasta väljad',
                           font=self.__default, command=self.__controller.clear_all_fields)
        clear_btn.grid(row=2, column=2, padx=5, pady=5, sticky=EW)

        return btn_search, open_btn, clear_btn

    def create_labels(self):
        lbl_form = Label(self.top_frame, text='2. Sisesta otsing: ', anchor='w', font=self.__default)
        lbl_form.grid(row=0, column=1, padx=5, pady=2, sticky=EW)

        open_file_lbl = Label(self.third_frame, bg='lightblue', text='Avatud fail:', anchor='w', font=self.__default)
        open_file_lbl.grid(row=0, column=0, padx=5, pady=2, sticky=EW)
        file_name_lbl = Label(self.third_frame, bg='lightblue', text='Fail pole valitud', anchor='w',
                              font=self.__default)
        file_name_lbl.grid(row=0, column=1, padx=5, pady=2, sticky=EW)

        lbl_entry_insert = Label(self.top_frame, text='Sisestatud otsingusõna',
                                 anchor='center', font=self.__default)
        lbl_entry_insert.grid(row=1, column=1, padx=5, pady=2, sticky=EW)

        row_count_lbl = Label(self.third_frame, text='Mitu rida kokku:', bg='lightblue',
                              anchor='w', font=self.__default)
        row_count_lbl.grid(row=0, column=2, padx=5, pady=2, sticky=EW)

        count_lbl = Label(self.third_frame, text='0', bg='lightblue', anchor='w', font=self.__default)
        count_lbl.grid(row=0, column=3, padx=5, pady=2, sticky=EW)

        error_lbl = Label(self.top_frame, text='', anchor='w', font=self.__default, bg="lightblue", fg="red")
        error_lbl.grid(row=2, column=0, padx=5, pady=2, columnspan=4, sticky=EW)
        return lbl_form, open_file_lbl, file_name_lbl, lbl_entry_insert, row_count_lbl, count_lbl, error_lbl

    def draw_search_result(self, header, data):
        if len(data) > 0:
            table = ttk.Treeview(self.bottom_frame)
            vsb = ttk.Scrollbar(self.bottom_frame, orient=VERTICAL, command=table.yview)
            vsb.pack(side=RIGHT, fill=Y)
            table.configure(yscrollcommand=vsb.set)

            table.heading('#0', text='№', anchor=W)
            table.column('#0', anchor=CENTER, width=2)

            column_ids = [h.lower() for h in header]
            table['columns'] = column_ids
            for h in header:
                table.heading(f'{h.lower()}', text=h, anchor=CENTER)
                table.column(f'{h.lower()}', anchor=CENTER, width=50)

            x = 1
            for d in data:
                table.insert(parent='', index=END, iid=str(x), text=str(x), values=d)
                x += 1
            table.pack(expand=True, fill=BOTH)

    def clear_insert(self):
        for widget in self.bottom_frame.winfo_children():
            widget.destroy()

    def clear(self, lbl_count_txt, error_lbl_txt):
        self.insert.delete(0, 'end')
        self.lbl_count['text'] = lbl_count_txt
        self.clear_insert()
        self.error_lbl['text'] = error_lbl_txt
