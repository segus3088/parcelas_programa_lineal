
from tkinter import *

from GUIFile import GUIFile

def main():
	window = Tk()
	sudoku_file = GUIFile(window)
	window.geometry("800x600+50+50")
	window.configure()
	window.mainloop()

if __name__ == '__main__':
	main()
