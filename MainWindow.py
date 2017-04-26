import tkinter as tk
from tkinter import ttk, filedialog


def setWindowProperties(paWindow):
    paWindow.title("Cloud template converter")
    # set width, height, x position, y position
    paWindow.geometry("400x200+300+150")
    #paWindow.resizable(False, False)
    # paWindow.configure(background='light grey')
    paWindow.iconbitmap(r'cloud-icon-full.ico')

    #
    labelFrom = tk.Label(paWindow, text="File from:")
    labelFrom.grid(row=0, column=0, sticky="w", padx=20)

    entryFrom = tk.Entry(paWindow)
    entryFrom.grid(row=1, column=0, columnspan=2, padx=20, ipadx=70, sticky="w")

    button1 = tk.Button(paWindow, text="Choose file", command=chooseFileDialog)
    button1.grid(row=1, column=2, sticky="w")

    labelFromFormat = tk.Label(paWindow, text="Input format:", padx=20)
    labelFromFormat.grid(row=2, column=0, sticky="w")

    comboInputFormat = ttk.Combobox(paWindow, state='readonly')
    comboInputFormat['values'] = ('A', 'B', 'C')
    comboInputFormat.grid(row=2, column=1, sticky="w")
    #comboInputFormat.current(0)



    labelTo = tk.Label(paWindow, text="File to:")
    labelTo.grid(row=3, column=0, sticky="w", padx=20)

    entryTo = tk.Entry(paWindow)
    entryTo.grid(row=4, column=0, columnspan=2, padx=20, ipadx=70, sticky="w")

    button2 = tk.Button(paWindow, text="Choose file", command=chooseFileDialog)
    button2.grid(row=4, column=2, sticky="w")

    labelToFormat = tk.Label(paWindow, text="Output format:", padx=20)
    labelToFormat.grid(row=5, column=0, sticky="w")

    comboOutputFormat = ttk.Combobox(paWindow, state='readonly')
    comboOutputFormat['values'] = ('D', 'E', 'F')
    comboOutputFormat.grid(row=5, column=1, sticky="w")
    #comboOutputFormat.current(0)





    buttonSubmit = tk.Button(paWindow, text="Make!", command=False)
    buttonSubmit.grid(row=6, column=2)


def chooseFileDialog():
    file = filedialog.askopenfilename()




if __name__ == "__main__":
    root = tk.Tk()
    setWindowProperties(root)
    root.mainloop()
