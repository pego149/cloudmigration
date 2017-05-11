import MainWindow as MainWindow
import tkinter as tk


def wheel(param1, param2, param3, param4):
    print("From: " + param1 + ", system " + param2)
    print("To: " + param3 + ", system " + param4)
    return 0


# Main method
if __name__ == "__main__":
    root = tk.Tk()

    if not MainWindow.setWindowProperties(root):
        MainWindow.infoWindow("error", "Error", "Error in creating main window.")
        exit(1)

    root.mainloop()
