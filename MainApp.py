import Tkinter as tk
import ttk

class App(tk.Tk):
	""" THe App class represents the entire app and is the master to all """
	def __init__(self,*args,**kwargs):
		tk.Tk.__init__(self,*args)

		self.title('Blood vessel printer')
		self.input_frame = tk.Frame(self,bg="green")



if __name__ == "__main__":
	app = App()
	app.mainloop()