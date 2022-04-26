import tkinter
from tkinter import ttk
import random
from tkinter import messagebox
import os

os.system('sh directory.sh')

class SelectMinMax:
    def __init__(self, path):
        self.path=path
        self.root = tkinter.Tk()
        self.root.geometry('500x500')
        self.root.maxsize(500, 400)
        self.root.minsize(500, 400)
        self.root.title('Select interval of numbers')
        self.root.configure(background='cyan')

        self.labels()
        self.entry()
        self.save()
        self.root.mainloop()

    def read(self):
        with open(f'{self.path}/minmax.txt', 'r') as file:
            return list(map(int, file.readline().split()))

    def labels(self):
        tkinter.Label(self.root, text='Select interval of numbers', background='yellow', foreground='navy',
                      font='Arial 20', width=20, height=2).place(x=250, y=50, anchor=tkinter.CENTER)

        tkinter.Label(self.root, text='MIN', background='yellow', foreground='navy',
                      font='Arial 20', width=15, height=1).place(x=250, y=150, anchor=tkinter.CENTER)

        tkinter.Label(self.root, text='MAX', background='yellow', foreground='navy',
                      font='Arial 20', width=15, height=1).place(x=250, y=250, anchor=tkinter.CENTER)
        try:
            mn,mx=self.read()
        except:
            return
            
        tkinter.Label(self.root, text=f'To play with interval {mn} to {mx}, press QUIT.', font='Arial 15', bg='red', fg='white').place(x=250, y=110, anchor=tkinter.CENTER)

    
    def entry(self):
        self.min = tkinter.Entry(self.root, background='yellow', foreground='navy', font='Arial 20', width=8)
        self.min.place(x=250, y=188, anchor='c')

        self.max = tkinter.Entry(self.root, background='yellow',
                            foreground='navy', font='Arial 20', width=8)
        self.max.place(x=250, y=288, anchor='c')
    
    def save(self):
        btn=tkinter.Button(self.root, text='Submit', background='yellow',width=6,
                           foreground='navy', font='Arial 18', command=self.return_min_max)
        btn.place(x=200, y=350, anchor=tkinter.CENTER)

        btn2 = tkinter.Button(self.root, text='QUIT', background='yellow', width=6,
                             foreground='navy', font='Arial 18', command=self.root.destroy)
        btn2.place(x=300, y=350, anchor=tkinter.CENTER)

    def return_min_max(self):
        try:
            mn = int(self.min.get())
            mx = int(self.max.get())
        except:
            return

        if mn < mx:
            self.min_val=mn
            self.max_val=mx
            with open(f'{self.path}/minmax.txt', 'w') as file:
                file.write(str(self.min_val)+' '+str(self.max_val))
            self.root.destroy()

class NumberGuessing:
    def __init__(self, path):
        self.path=path
        SelectMinMax(self.path)
        self.min,self.max = self.read()
        self.act_value=''
        self.counter=1
        self.guessed_num=random.randint(self.min,self.max)

        self.root=tkinter.Tk()
        self.root.geometry('500x500')
        self.root.maxsize(500,500)
        self.root.minsize(500, 500)
        self.root.title('Number Guessing Game')
        self.root.configure(background='cyan')

        self.create_labels()
        self.create_entry()
        self.create_buttons()
        self.tree.bind('<ButtonRelease-1>', self.selectItem)

    def read(self):
        with open(f'{self.path}/minmax.txt', 'r') as file:
            return list(map(int, file.readline().split()))

    def create_labels(self):
        tkinter.Label(self.root,text='Number Guessing Game', background='yellow', foreground='navy', font='Arial 20', width=20,height=2).place(x=250,y=50,anchor=tkinter.CENTER)
        
        tkinter.Label(self.root, text=f'Guess a number between\n {self.min} and {self.max}', background='yellow', foreground='navy',
                      font='Arial 15', width=21, height=2).place(x=250, y=110, anchor=tkinter.CENTER)

    def create_buttons(self):
        yes = tkinter.Button(self.root, text='Confirm Guess', background='yellow', foreground='navy', font='Arial 18', command=self.check_num)
        yes.place(x=250,y=450, anchor=tkinter.CENTER)

    def create_entry(self):
        self.tree = ttk.Treeview(self.root, selectmode='browse')
        self.tree.place(x=250,y=280,anchor=tkinter.CENTER)

        scrlbr = ttk.Scrollbar(self.root,
                                   orient="vertical",
                                   command=self.tree.yview)
        scrlbr.place(x=291, y=250)

        self.tree.configure(xscrollcommand=scrlbr.set)

        self.tree["columns"] = ("1")

        self.tree['show']=('headings')
        self.tree.column("1",width=80, anchor='c')
        self.tree.heading('1',text='Number')
        self.insert()

    def insert(self):
        for i in range(self.min,self.max+1):
            self.tree.insert('','end',text=i,values=(i),tags=i)
    
    def selectItem(self,a):
        curItem = self.tree.focus()
        self.act_value = self.tree.item(curItem)
    
    def your_guess(self, eq):
        try:
            lbl.destroy()
        except:
            pass

        lbl=tkinter.Label(self.root, text=f'Your guessed number is {eq} than secret number.', font='Arial 16').place(x=250,y=410, anchor=tkinter.CENTER)

    def check_num(self):
        if self.act_value!='':
            try:
                val = int(self.act_value['text'])
            except:
                return

            if val > self.guessed_num:
                self.your_guess('greater')
            elif val< self.guessed_num:
                self.your_guess('lower')
            
            else:
                msg=messagebox.askyesno(title='CONGRATULATION, YOU GUESSED THE SECRET NUMBER', message=f'It took you {self.counter}. tries.\nDo you want to play again?')
                self.root.destroy()
                if msg:
                    self.__init__(self.path)
                return

            self.counter+=1
            self.tree.delete(self.tree.selection()[0])
            self.act_value=''


NumberGuessing(open('directory.txt', 'r').readline().strip()[2:])
tkinter.mainloop()
