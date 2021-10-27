from os import system
from tkinter.filedialog import askopenfilename
from tkinter import Tk


root = Tk()
root.withdraw()
file = askopenfilename(filetypes =[('Python Files', '*.py')])

if file != '':
    system('python3 ' + file)
else:
    print('Please select a valid file')
