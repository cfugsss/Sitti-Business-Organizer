import sqlite3

class db:
    def __init__(self):
        self.conn = sqlite3.connect("sittiusers.db")
        self.curs = self.conn.cursor()

    def createUser(self, username, email, password):
        self.curs.execute(
            "INSERT INTO users (username, email, password)" "VALUES(?,?,?)", (username, email, password)
        )
        self.conn.commit()

    def confirm(self, username, password):
        self.curs.execute("SELECT * FROM users where username = ?", [username])
        account = self.curs.fetchone()
        print(account)
        try:
            if account[1] is None:
                return 2
        except TypeError:
            return 2
        if username == account[1] and password == str(account[3]):
            return 1
        else:
            return 3

    def checkEmail(self, email):
        self.curs.execute("SELECT * FROM users where email = ?", [email])
        result = self.curs.fetchone
        if result:
            return 1
        else:
            return 2

    def passwordUpdate(self, email, passw):
        self.curs.execute("UPDATE users set password = ? where email = ?", [passw, email])
        self.conn.commit()
        self.curs.execute("SELECT * FROM users where password = ?", [passw])
        result = self.curs.fetchone
        if result:
            return 1
        else:
            return 2



