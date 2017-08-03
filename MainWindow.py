import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import CloudMigration as CloudMigration


def openFileDialog(param):
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


def saveFileDialog(param):
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


def setWindowProperties(self, cloudTypes):
    """
    Sets main window properties
    :param self: window, which will be adjusted
    :param cloudTypes: names of all actively linked modules
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

    buttonFileFrom = tk.Button(self, text="Choose file", command=lambda: openFileDialog(entryFrom))
    buttonFileFrom.grid(row=1, column=2, sticky="w")

    labelFromFormat = tk.Label(self, text="Input format:", padx=20)
    labelFromFormat.grid(row=2, column=0, sticky="w")

    comboInputFormat = ttk.Combobox(self, state='readonly', values=cloudTypes)
    comboInputFormat.grid(row=2, column=1, sticky="w")
    comboInputFormat.current(0)

    # second part about output file
    labelTo = tk.Label(self, text="File to:")
    labelTo.grid(row=3, column=0, sticky="w", padx=20)

    entryTo = tk.Entry(self)
    entryTo.grid(row=4, column=0, columnspan=2, padx=20, ipadx=70, sticky="w")

    buttonFileTo = tk.Button(self, text="Choose file", command=lambda: saveFileDialog(entryTo))
    buttonFileTo.grid(row=4, column=2, sticky="w")

    labelToFormat = tk.Label(self, text="Output format:", padx=20)
    labelToFormat.grid(row=5, column=0, sticky="w")

    comboOutputFormat = ttk.Combobox(self, state='readonly', values=cloudTypes)
    comboOutputFormat.grid(row=5, column=1, sticky="w")
    comboOutputFormat.current(0)

    ##### test purposes
    entryFrom.insert(0, "C:/Users/marek/Documents/cloud/puppetmaster.template")
    entryTo.insert(0, 'C:/Users/marek/Documents/cloud/test-openstack.yaml')
    comboInputFormat.current(1)
    comboOutputFormat.current(2)
    ######

    # last part, execute button
    buttonSubmit = tk.Button(self, text="Make!",
                             command=lambda: CloudMigration.doTransformation(entryFrom.get(), comboInputFormat.get(),
                                                                             entryTo.get(), comboOutputFormat.get()))
    buttonSubmit.grid(row=6, column=2)

    # Binding "Enter" key to submit button and getting focus to the button
    buttonSubmit.bind('<Return>', lambda event: CloudMigration.doTransformation(entryFrom.get(), comboInputFormat.get(),
                                                                                entryTo.get(), comboOutputFormat.get()))
    self.bind('<Return>', buttonSubmit.focus_set())

    return True


def infoWindow(messageType, message, *args):
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
