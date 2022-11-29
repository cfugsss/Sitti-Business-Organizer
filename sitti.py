from tkinter import ttk, Tk, RIDGE, messagebox
from tkcalendar import DateEntry
from PIL import ImageTk, Image
import sittidb
import otk
import emailotk
import sqlite3

class gui:
    def __init__(self, win):
        # storing classes from helper files in variables
        self.win = win
        self.db = sittidb.db()
        self.otk = otk.emailKey()
        self.email = emailotk.emailauto()
        self.main()

    def main(self):
        #build initial login page
        self.win.geometry("650x450")
        self.win.title("Sitti Business Pro")

        #creating header frame which holds logo and page title
        self.header = ttk.Frame(self.win)
        self.header.pack()
        self.orig = Image.open("logo.png")
        self.img = self.orig.resize((400, 60))
        self.logo = ImageTk.PhotoImage(self.img)
        ttk.Label(self.header, image = self.logo).grid(row=0,pady=10,padx=5)
        ttk.Label(self.header, text="Login", font=("Cambria", 22)).grid(row=1,column=0,padx=5,pady=10)

        #creating body and buttons frame which contains entries, labels, and buttons
        self.body = ttk.Frame(self.win)
        self.body.config(relief=RIDGE)
        self.body.pack()
        ttk.Label(self.body, text="Username").grid(row=0,column=0,pady=10,padx=10)
        self.logUser = ttk.Entry(self.body)
        self.logUser.grid(row=0,column=1,columnspan=2,pady=10,padx=10)
        ttk.Label(self.body, text="Password").grid(row=1,column=0,pady=10,padx=10)
        self.logPass = ttk.Entry(self.body)
        self.logPass.grid(row=1,column=1,columnspan=2,pady=10,padx=10)

        self.buttons = ttk.Frame(self.win)
        self.buttons.pack()
        self.create = ttk.Button(self.buttons, text="Create Account", command=self.createAcc)
        self.create.grid(row=0,column=0,columnspan=2,pady=10,padx=5)
        self.login = ttk.Button(self.buttons, text="Login", command=self.loginCheck)
        self.login.grid(row=0,column=2,columnspan=2,pady=10,padx=5)
        self.forgotPassw = ttk.Button(self.buttons, text="Forgot Password", width=25, command=self.forgotPass)
        self.forgotPassw.grid(row=1,column=1,columnspan=2,pady=10,padx=5)

    def forgotPass(self):
        # clears login page to start creating a forgot password page
        self.header.forget()
        self.body.forget()
        self.buttons.forget()
        # generate otk // probably change this and get email wokring
        self.genOTK = self.otk.getKey()

        #set heading for forgot password page
        self.header = ttk.Frame(self.win)
        self.header.pack()
        self.orig = Image.open("logo.png")
        self.img = self.orig.resize((400, 60))
        self.logo = ImageTk.PhotoImage(self.img)
        ttk.Label(self.header, image = self.logo).grid(row=0,pady=10,padx=5)
        ttk.Label(self.header, text="Forgot Password", font=("Cambria", 22)).grid(row=1,column=0,padx=5,pady=10)

        #body frame --> takes in email to check for account and send otp
        self.body = ttk.Frame(self.win)
        self.body.pack()
        ttk.Label(self.body, text="Enter Email: ").grid(row=0,column=0,pady=10,padx=10)
        self.fpemail = ttk.Entry(self.body)
        self.fpemail.grid(row=0,column=1,padx=10,pady=10)

        ttk.Button(self.body, text="Send OTK", width=25, command=self.chendKey).grid(row=1,column=0,columnspan=2,pady=10,padx=10)

    def chendKey(self):
        #chendKey --> check + send key
        #storing email given by user in variable
        self.chkmail = self.fpemail.get()
        #running email given through function to check if said email is registered to an account
        self.emailtoken = self.db.checkEmail(self.chkmail)
        #function returns 2 -> no account returned with that email --> returns to main page
        if self.emailtoken == 2:
            messagebox.showinfo(title="INVALID", message="No account with that email in use")
            self.header.forget()
            self.body.forget()
            self.main()
        #function returns 1 --> account found --> otp sent to email given by user
        if self.emailtoken == 1:
            self.body.forget()
            self.body = ttk.Frame(self.win)
            self.body.pack()
            self.email.sendOTK(self.chkmail)

            ttk.Label(self.body, text="Enter key from email: ").grid(row=0,column=0,columnspan=2,padx=10,pady=10)
            self.entryKey = ttk.Entry(self.body)
            self.entryKey.grid(row=0,column=2, columnspan=2,padx=10,pady=10)
            ttk.Button(self.body, text="Submit", command=self.changePass).grid(row=1,column=1,pady=10,padx=10)

    def changePass(self):
        # checking key given by user to key function by app
        self.otkcheck = self.entryKey.get()
        self.otkToken = self.otk.check(self.otkcheck,self.genOTK)
        # function returned 2 --> incorrect otp --> user sent back to main
        if self.otkToken == 2:
            messagebox.showinfo(title="INVALID", message="OTK does not match")
            self.header.forget()
            self.body.forget()
            self.main()
        # function returned 1 --> otps match and user can choose new password
        if self.otkToken == 1:
            messagebox.showinfo(title="SUCCESS", message="Create new password")
            self.header.forget()
            self.header = ttk.Frame(self.win)
            self.header.pack()
            self.orig = Image.open("logo.png")
            self.img = self.orig.resize((400, 60))
            self.logo = ImageTk.PhotoImage(self.img)
            ttk.Label(self.header, image = self.logo).grid(row=0,pady=10,padx=5)
            ttk.Label(self.header, text="New Password", font=("Cambria", 22)).grid(row=1,column=0,padx=5,pady=10)
            self.body.forget()
            self.body = ttk.Frame(self.win)
            self.body.pack()
            ttk.Label(self.body, text="New Password: ").grid(row=0,column=0,pady=10,padx=10)
            self.newPassword = ttk.Entry(self.body)
            self.newPassword.grid(row=0,column=1,columnspan=2,padx=10,pady=10)
            ttk.Button(self.body, text="Submit", command=self.chngPass).grid(row=1,column=1,pady=10,padx=10)


    def chngPass(self):
        #on user submit --> new password sent to db function to replacce password
        self.newPassUpdate = self.newPassword.get()
        self.chngToken = self.db.passwordUpdate(self.newPassUpdate, self.chkmail)
        #same function from above returns 1 for a failed replacement and 2 for a successfull replacement
        if self.chngToken == 2:
            messagebox.showinfo(title="INVALID", message="password update failed")
            self.header.forget()
            self.body.forget()
            self.main()
        if self.chngToken == 1:
            messagebox.showinfo(title="SUCCESS", message="password changed")
            self.header.forget()
            self.body.forget()
            self.main()



    def createAcc(self):
        self.header.forget()
        self.body.forget()
        self.buttons.forget()

        #new heading frame
        self.header = ttk.Frame(self.win)
        self.header.pack()
        self.orig = Image.open("logo.png")
        self.img = self.orig.resize((400, 60))
        self.logo = ImageTk.PhotoImage(self.img)
        ttk.Label(self.header, image = self.logo).grid(row=0,pady=10,padx=5)
        ttk.Label(self.header, text="Enter Details", font=("Cambria", 18)).grid(row=1,column=0,padx=5,pady=10)

        #body frame - get information for account
        self.body = ttk.Frame(self.win)
        self.body.pack()
        ttk.Label(self.body, text="Username: ").grid(row=0,column=0,pady=7,padx=5)
        self.nuser = ttk.Entry(self.body)
        self.nuser.grid(row=0,column=1,pady=7,padx=5)
        ttk.Label(self.body, text="Password: ").grid(row=1,column=0,pady=7,padx=5)
        self.npass = ttk.Entry(self.body)
        self.npass.grid(row=1,column=1,pady=7,padx=5)
        ttk.Label(self.body, text="Email: ").grid(row=2,column=0,padx=7,pady=5)
        self.nmail = ttk.Entry(self.body)
        self.nmail.grid(row=2,column=1,pady=7,padx=5)

        #body frame - create button
        ttk.Button(self.body, text="Create Account", command=self.checkNew).grid(row=3,column=0,columnspan=2,pady=7,padx=5)

    def checkNew(self):
        #get user details for account
        self.cuser = self.nuser.get()
        self.cpass = self.npass.get()
        self.cmail = self.nmail.get()
        # function tries adding user to db except for an error caused by not having unique email or username
        try:
            self.db.createUser(self.cuser, self.cmail, self.cpass)
            messagebox.showinfo(title="SUCCESS", message="account was created, {}".format(self.cuser))
            self.header.forget()
            self.body.forget()
            self.main()
        except sqlite3.IntegrityError:
            messagebox.showinfo(title="INVALID", message="Username or Email in use")
            self.createAcc()

    def mainProgram(self):
        self.header = ttk.Frame(self.win)
        self.header.pack()
        self.orig = Image.open("logo.png")
        self.img = self.orig.resize((400, 60))
        self.logo = ImageTk.PhotoImage(self.img)
        ttk.Label(self.header, image = self.logo).grid(row=0,pady=10,padx=5)

        self.body = ttk.Frame(self.win)
        self.body.pack()

        ttk.Button(self.body, text="button 1", width=50).grid(column=0,columnspan=2,row=0,padx=15,pady=15)
        ttk.Button(self.body, text="button 2", width=50).grid(column=0,columnspan=2,row=1,padx=15,pady=15)
        ttk.Button(self.body, text="button 3", width=50).grid(column=0,columnspan=2,row=2,padx=15,pady=15)
        ttk.Button(self.body, text="button 4", width=50).grid(column=0,columnspan=2,row=3,padx=15,pady=15)
        ttk.Button(self.body, text="button 5", width=50).grid(column=0,columnspan=2,row=4,padx=15,pady=15)
        




    def loginCheck(self):
        #get user details from login page
        self.chkusr = self.logUser.get()
        self.chkpas = self.logPass.get()

        #function returns a token with values either 1, 2, 3
        self.token = self.db.confirm(self.chkusr, self.chkpas)
        # value 2 represents - no such account recognized (no username in db)
        if self.token == 2:
            self.header.forget()
            self.body.forget()
            self.buttons.forget()
            self.main()
            messagebox.showinfo(title="INVALID", message="No account created")
        # value 3 represents - a password OR username was recognized in the db however both do not match
        if self.token == 3:
            self.header.forget()
            self.body.forget()
            self.buttons.forget()
            self.main()
            messagebox.showinfo(title="INVALID", message="Username or Password incorrect")
        #value of 1 represents a match of both username AND password --> granted access to dashboard
        if self.token == 1:
            messagebox.showinfo(title="SUCCESS", message="Logged-in: {}".format(self.chkusr))
            self.header.forget()
            self.body.forget()
            self.buttons.forget()
            self.mainProgram()



#SAM BUILD HERE






root = Tk()
gui(root)

root.mainloop() 
        