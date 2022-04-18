import tkinter as tk
from tkinter import ttk
from tkinter import END
from frame.mointer.listenerApp import App

#
# class App:
#     def __init__(self, master):
#         style = ttk.Style()# tabposition='wn'
#         Mysky = "#DCF0F2"
#         Myyellow = "#F2C84B"
#         style.theme_create("dummy", parent="alt", settings={
#             "TNotebook": {"configure": {"tabmargins": [2, 15, 2, 2],"tabposition":'wn',}},
#             "TNotebook.Tab": {
#                 "configure": {"padding": [5, 10], "background": 'white','font':['仿宋', 14],'width':8},
#                 "map": {"background": [("selected", Mysky)],
#                         "expand": [("selected", [1, 1, 1, 0])]}
#             }
#         })
#         style.theme_use("dummy")
#         self.notebook = ttk.Notebook(master)
#         self.frame1 = tk.Frame(master,bg = "red")
#         self.frame2 = tk.Frame(master,bg = "blue")
#         self.frame3 = tk.Frame(master,bg = "black")
#         self.frame4 = tk.Frame(master)
#
#         self.notebook.add(self.frame1, text='system',padding=10)
#         self.notebook.add(self.frame2, text='listener',padding=10)
#         self.notebook.add(self.frame3, text='editor',padding=10)
#         self.notebook.add(self.frame4, text='setup',padding=10)
#         self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True,side='left')
#
#
