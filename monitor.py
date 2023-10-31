from tkinter import *
from processor import response_handler

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
bot_name = "GMRE bot"

class ChatApp:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("GMRE Chatbot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470,height=550, bg=BG_COLOR)

        sub_title = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        sub_title.place(relwidth=1)


        hline = Label(self.window,width=450, bg=BG_GRAY)
        hline.place(relwidth=1,rely=0.07,relheight=0.012)

        self.chats = Text(self.window,width=20,height=2,bg=BG_COLOR,fg=TEXT_COLOR, font=FONT, padx=5,pady=5)
        self.chats.place(relheight=0.745,relwidth=1,rely=0.08)
        self.chats.configure(cursor="arrow",state=DISABLED)

        scrollbar = Scrollbar(self.chats)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.chats.yview)

        bottom_label = Label(self.window,bg=BG_GRAY,height=80)
        bottom_label.place(relwidth=1,rely=0.825)
        
        self.msg_box = Entry(bottom_label, bg="#2C3E50",fg=TEXT_COLOR, font=FONT)
        self.msg_box.place(relwidth=0.74,relheight=0.06,rely=0.008, relx=0.011)
        self.msg_box.focus()
        self.msg_box.bind("<Return>",self._handle_msg)

        #send_btn = Button(bottom_label, text="Send", font=FONT_BOLD, width20, bg=BG_GRAY, command=lambda:self._handle_msg(None))
        #send_btn.place(relx=0.77,rely=0.008,relheight=0.006,relwidth=0.22)

    def _handle_msg(self,event):
        msg = self.msg_box.get()
        self._insert_msg(msg,"You")

    def _insert_msg(self,msg,sender):
        if not msg:
            return

        self.msg_box.delete(0, END)
        res = f"{sender}: {msg}\n\n"
        self.chats.configure(state=NORMAL)
        self.chats.insert(END,res)
        self.chats.configure(state=DISABLED)

        bot_res = f"{bot_name}: {response_handler(msg)}\n\n"
        self.chats.configure(state=NORMAL)
        self.chats.insert(END,bot_res)
        self.chats.configure(state=DISABLED)

        self.chats.see(END)

if __name__ == "__main__":
    app = ChatApp()
    app.run()

# def send_message():
#     pass

# app = Tk()

# msg_label = Label(app,text="Enter Text", font=('bold',14),pady=20,padx=20)
# msg_label.grid(row=0,column=0,sticky=W)

# input_txt = StringVar()
# input_msg = Entry(app, textvariable=input_txt)
# input_msg.grid(row=0,column=1)

# send_btn = Button(app,text="Send", width=12, command=send_message)
# send_btn.grid(row=2,column=0, pady=20)

# app.title('GMRE Chatbot')
# app.geometry('350x700')

# app.mainloop()