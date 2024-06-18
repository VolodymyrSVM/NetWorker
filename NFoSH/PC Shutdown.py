import os
import customtkinter as ctk
#from PIL import Image
import sys

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('PC Shutdown')
        self.geometry("650x200")
        self.resizable(0,0)
        #self.config(bg='#ffffff', ) # Задній фон
        self.pc_names = ['01', '02', '03', '04', '05',
                         '06', '07', '08', '09', '10',
                         '11', '12', '13', '14', '15']
        #img = ctk.CTkImage(dark_image=Image.open(r"update.png"))
        
        self.pc_chosen_frame = CheckboxFrame(self, self.pc_names)
        self.pc_chosen_frame.grid(row=0, column=0, padx=10, pady=10)
        self.yes_btn = ctk.CTkButton(self, text='Shut down chosen PC', command=self.pc_off)
        self.yes_btn.grid(row=1, column=0, padx=20)
        
    def pc_off(self):
        pc_list = self.pc_chosen_frame.take_checkbox()
        #print(pc_list)
        for i in pc_list:
            if i=='PC-01':
                continue
            os.system('Shutdown /s -m \\\\'+i)
            for chk in self.pc_chosen_frame.pc_checkboxes:
                if chk.cget("text") == i:
                    chk.deselect()
                    chk.configure(state='disabled')
            self.pc_chosen_frame.checkbtn_allpc.deselect()
        if 'PC-01' in pc_list:
            os.system('Shutdown /s ')
            sys.exit()
        
class CheckboxFrame(ctk.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)

        self.checkbtn_allpc = ctk.CTkCheckBox(self, text='All PC', command=self.choose_all)
        self.checkbtn_allpc.grid(row=0, column=0, columnspan=5, pady = 10)
        self.upd_btn = ctk.CTkButton(self, text='Update', command=self.update_checkbox)
        self.upd_btn.grid(row=0, column=4, padx=20)
        ## Можна спробувати демонструвати тільки ті які бачить мережа
        self.values = values
        
        self.pc_checkboxes = []
        for i, val in enumerate(self.values):
            checkbtn = ctk.CTkCheckBox(self, text='PC-'+val, height=1)
            checkbtn.grid(row=i//5+1, column=i%5, padx=10, pady=(5,0))
            self.pc_checkboxes.append(checkbtn)
        self.update_checkbox()
    def choose_all(self):
        if self.checkbtn_allpc.get()==1:
            for chk in self.pc_checkboxes:
                if chk.cget('state')=='disabled':
                    continue
                chk.select()
        else:
            for chk in self.pc_checkboxes:
                chk.deselect()

    def take_checkbox(self):
        chosen_pc = []
        for checkbox in self.pc_checkboxes:
            if checkbox.get() == 1:
                chosen_pc.append(checkbox.cget("text"))
        # print(chosen_pc)
        return chosen_pc
    
    def update_checkbox(self):
        # up_wind = UpdateWindow(self)
        # up_wind.mainloop()
        #print(1)
        self.checkbtn_allpc.deselect()
        for checkbox in self.pc_checkboxes:
            checkbox.deselect()
            txt = checkbox.cget("text")
            if txt=='PC-01': continue
            with open("ping.txt", "w") as ping:
                pass
            ping.close()
            os.system('ping -n 1 -a '+txt+" >> ping.txt")
            with open("ping.txt", "r") as ping:
                uns = ping.read()
            ping.close()
            print(uns)
            if 'Received = 1' in uns:
                checkbox.configure(state='normal')
            else:
                checkbox.configure(state='disabled')
        
class UpdateWindow(ctk.CTkToplevel):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("300x150")
        self.title('Updating')

        self.label = ctk.CTkLabel(self, text="Updating in progress")
        self.label.pack(padx=20, pady=20)
    
app =  App()
app.mainloop()
