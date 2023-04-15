import logging
import pathlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext

class MainWindow:
    def __init__(self, window, cloudTypes, doTransformation):
        """
        Sets main window properties
        :param self: window, which will be adjusted
        :param cloudTypes: names of all actively linked modules
        :return: boolean value of success
        """

        # global window settings
        window.title("Cloud template converter")
        # set width, height, x position, y position
        window.geometry("663x545")
        window.resizable(False, False)
        window.iconbitmap(r'cloudmigration\Pictures\cloud-icon-full.ico')

        # first part about input file
        labelFrom = tk.Label(window, text="File from:")
        labelFrom.grid(row=0, column=0, sticky="w", padx=20)

        entryFrom = tk.Entry(window)
        entryFrom.grid(row=1, column=0, columnspan=3, padx=20, ipadx=120, sticky="w")

        buttonFileFrom = tk.Button(window, text="Choose file", command=lambda: self.openFileDialog(entryFrom))
        buttonFileFrom.grid(row=1, column=2, sticky="w")

        labelFromFormat = tk.Label(window, text="Input format:", padx=20)
        labelFromFormat.grid(row=2, column=0, sticky="w")

        comboInputFormat = ttk.Combobox(window, state='readonly', values=cloudTypes)
        comboInputFormat.grid(row=2, column=1, sticky="w")
        comboInputFormat.current(0)

        ttk.Separator(window, orient=tk.HORIZONTAL).grid(row=3, column=0, padx=20, ipadx=240, columnspan=3, pady=10)

        # second part about output file
        labelTo = tk.Label(window, text="File to:")
        labelTo.grid(row=4, column=0, sticky="w", padx=20)

        entryTo = tk.Entry(window)
        entryTo.grid(row=5, column=0, columnspan=2, padx=20, ipadx=120, sticky="w")

        buttonFileTo = tk.Button(window, text="Choose file", command=lambda: self.saveFileDialog(entryTo))
        buttonFileTo.grid(row=5, column=2, sticky="w")

        labelToFormat = tk.Label(window, text="Output format:", padx=20)
        labelToFormat.grid(row=6, column=0, sticky="w")

        comboOutputFormat = ttk.Combobox(window, state='readonly', values=cloudTypes)
        comboOutputFormat.grid(row=6, column=1, sticky="w")

        ##### test purposes
        entryFrom.insert(0, "C:/Users/pego1/PycharmProjects/cloudmigration/input.yml")
        entryTo.insert(0, "C:/Users/pego1/PycharmProjects/cloudmigration/arm_test.json")
        comboInputFormat.current(2)
        comboOutputFormat.current(3)
        ######

        # last part, execute button
        buttonSubmit = tk.Button(window, text="Make!",
                                 command=lambda: doTransformation(self.getFileType(entryFrom.get()), entryFrom.get(),
                                                                  comboInputFormat.get(),
                                                                  self.getFileType(entryTo.get()),
                                                                  entryTo.get(), comboOutputFormat.get()))
        buttonSubmit.grid(row=5, column=3, sticky="we", padx=20)

        # Binding "Enter" key to submit button and getting focus to the button
        buttonSubmit.bind('<Return>', lambda event: doTransformation(self.getFileType(entryFrom.get()), entryFrom.get(),
                                                                     comboInputFormat.get(),
                                                                     self.getFileType(entryTo.get()),
                                                                     entryTo.get(), comboOutputFormat.get()))
        window.bind('<Return>', buttonSubmit.focus_set())

        st = tk.scrolledtext.ScrolledText(window, state='disabled')
        st.grid(row=7, column=0, sticky="w", columnspan=4)

        # Create textLogger
        text_handler = self.TextHandler(st)

        # Add the handler to logger
        self.logger = logging.getLogger()
        self.logger.addHandler(text_handler)
        self.logger.setLevel(logging.DEBUG)

    def openFileDialog(self, param):
        """
        Sets file name into parameter
        :param param: object, to which is file name inserted
        :return: boolean value of success
        """
        file = filedialog.askopenfilename(filetypes=[('JSON', ('*.json', '*.template'),), ('YAML', ('*.yaml', '*.yml'),),
                                                     ('Text', '*.txt',), ('Generic', '*.generic',), ('All Files', '.*')])
        # delete entry
        param.delete(0, 'end')
        # insert file name into entry
        param.insert(0, file)

        return True


    def saveFileDialog(self, param):
        """
        Sets file name into parameter
        :param param: object, to which is file name inserted
        :return: boolean value of success
        """
        file = filedialog.asksaveasfilename(filetypes=[('JSON', ('*.json', '*.template'),), ('YAML', ('*.yaml', '*.yml'),),
                                                       ('Generic', '*.generic',)])
        # delete entry
        param.delete(0, 'end')
        # insert file name into entry
        param.insert(0, file)

        return True

    def getLogger(self):
        return self.logger

    def getFileType(self, filename):
        """
        Gives type of file
        :param filename: name of file
        :return: type of file
        """

        if pathlib.Path(filename).suffix == ".yaml" or pathlib.Path(filename).suffix == ".yml":
            return "YAML"
        elif pathlib.Path(filename).suffix == ".json":
            return "JSON"
        else:
            return None

    def infoWindow(self, messageType, message, *args):
        """
        Function, that shows message window with a custom message
        :param messageType: Type of message (error, warning, info)
        :param message: Body of message
        :param args: first optional argument is window title
        :return:
        """
        if messageType == "error":
            if not args:
                messagebox.showerror("Error", message)
            else:
                messagebox.showerror(args[0], message)
        elif messageType == "warning":
            if not args:
                messagebox.showwarning("Warning", message)
            else:
                messagebox.showwarning(args[0], message)
        else:
            if not args:
                messagebox.showinfo("Information", message)
            else:
                messagebox.showinfo(args[0], message)


    class TextHandler(logging.Handler):
        """This class allows you to log to a Tkinter Text or ScrolledText widget"""

        def __init__(self, text):
            # run the regular Handler __init__
            logging.Handler.__init__(self)
            # Store a reference to the Text it will log to
            self.text = text

        def emit(self, record):
            msg = self.format(record)

            def append():
                self.text.configure(state='normal')
                self.text.insert(tk.END, msg + '\n')
                self.text.configure(state='disabled')
                # Autoscroll to the bottom
                self.text.yview(tk.END)

            # This is necessary because we can't modify the Text from other threads
            self.text.after(0, append)
