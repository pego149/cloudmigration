import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import CloudMigration as CloudMigration


def chooseFileDialog(param):
    """
    Sets file name into parameter
    :param param: object, to which is file name inserted
    :return: boolean value of success
    """
    file = filedialog.askopenfilename()
    # delete entry
    param.delete(0, 'end')
    # insert file name into entry
    param.insert(0, file)

    return True


def setWindowProperties(self):
    """
    Sets window properties
    :param self: window, which will be adjusted
    :return: boolean value of success
    """

    # global window settings
    self.title("Cloud template converter")
    # set width, height, x position, y position
    self.geometry("400x200+300+150")
    self.resizable(False, False)
    self.iconbitmap(r'Pictures\cloud-icon-full.ico')

    # first part about input file
    labelFrom = tk.Label(self, text="File from:")
    labelFrom.grid(row=0, column=0, sticky="w", padx=20)

    entryFrom = tk.Entry(self)
    entryFrom.grid(row=1, column=0, columnspan=2, padx=20, ipadx=70, sticky="w")

    buttonFileFrom = tk.Button(self, text="Choose file", command=lambda: chooseFileDialog(entryFrom))
    buttonFileFrom.grid(row=1, column=2, sticky="w")

    labelFromFormat = tk.Label(self, text="Input format:", padx=20)
    labelFromFormat.grid(row=2, column=0, sticky="w")

    comboInputFormat = ttk.Combobox(self, state='readonly')
    comboInputFormat['values'] = ('A', 'B', 'C')
    comboInputFormat.grid(row=2, column=1, sticky="w")
    comboInputFormat.current(0)

    # second part about output file
    labelTo = tk.Label(self, text="File to:")
    labelTo.grid(row=3, column=0, sticky="w", padx=20)

    entryTo = tk.Entry(self)
    entryTo.grid(row=4, column=0, columnspan=2, padx=20, ipadx=70, sticky="w")

    buttonFileTo = tk.Button(self, text="Choose file", command=lambda: chooseFileDialog(entryTo))
    buttonFileTo.grid(row=4, column=2, sticky="w")

    labelToFormat = tk.Label(self, text="Output format:", padx=20)
    labelToFormat.grid(row=5, column=0, sticky="w")

    comboOutputFormat = ttk.Combobox(self, state='readonly')
    comboOutputFormat['values'] = ('D', 'E', 'F')
    comboOutputFormat.grid(row=5, column=1, sticky="w")
    comboOutputFormat.current(0)

    # last part, execute button
    buttonSubmit = tk.Button(self, text="Make!",
                             command=lambda: CloudMigration.wheel(entryFrom.get(), comboInputFormat.get(),
                                                                  entryTo.get(), comboOutputFormat.get()))
    buttonSubmit.grid(row=6, column=2)

    return False


def infoWindow(messageType, title, message):
    """
    Function, that shows message window with a custom message
    :param messageType: Type of message (error, warning, info)
    :param title: Title of window
    :param message: Body of message
    :return: 
    """
    if messageType == "error":
        messagebox.showerror(title, message)
    elif messageType == "warning":
        messagebox.showwarning(title, message)
    else:
        messagebox.showinfo(title, message)
