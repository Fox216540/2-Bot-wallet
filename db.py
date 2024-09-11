import sqlite3

import db


def exchange():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    exchange = cursor_obj.execute("SELECT exchange FROM money").fetchall()[0][0]
    connection_obj.commit()
    connection_obj.close()
    return exchange
def add(id,ref,year,month,day):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()

    if ref != None:
        quant = cursor_obj.execute("SELECT quant FROM users WHERE id = ?",(ref,)).fetchall()[0][0]
        balance = cursor_obj.execute("SELECT earned FROM users WHERE id = ?",(ref,)).fetchall()[0][0]
        print(balance,exchange())
        cursor_obj.execute(f'UPDATE users SET quant = ?, earned = ? WHERE id = ?', (int(quant)+1,float(balance)+float(exchange()),ref))
    cursor_obj.execute("INSERT INTO users (id,ref,year,month,day,quant,earned,salary) VALUES(?,?,?,?,?,?,?,?)", (id, ref, year, month, day, 0, 0, 0))
    connection_obj.commit()
    connection_obj.close()
    return True

def change(text):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute(f'UPDATE mailing SET text1 = ?', (text,))
    connection_obj.commit()
    connection_obj.close()

def change2(text):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute(f'UPDATE mailing SET text2 = ?', (text,))
    connection_obj.commit()
    connection_obj.close()

def text():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = cursor_obj.execute(f'SELECT text1 FROM mailing').fetchall()[0][0]
    connection_obj.commit()
    connection_obj.close()
    return text

def text2():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = cursor_obj.execute(f'SELECT text2 FROM mailing').fetchall()[0][0]
    connection_obj.commit()
    connection_obj.close()
    return text


def users():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = cursor_obj.execute("SELECT id FROM users").fetchall()
    connection_obj.commit()
    connection_obj.close()
    return text



def personal_account(user_id):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    quant,salary = cursor_obj.execute("SELECT quant,salary FROM users WHERE id = ?",(user_id,)).fetchall()[0]
    earned = cursor_obj.execute("SELECT earned FROM users WHERE id = ?",(user_id,)).fetchall()[0][0]
    connection_obj.commit()
    connection_obj.close()
    return quant,earned,salary

def withdraw(user_id,money):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    earned = cursor_obj.execute("SELECT earned FROM users WHERE id = ?",(user_id,)).fetchall()[0][0]
    money_user = "%.4f" % (float(earned)-float(money))
    cursor_obj.execute(f'UPDATE users SET earned = ? WHERE id = ?', (money_user, user_id))
    connection_obj.commit()
    salary = cursor_obj.execute("SELECT salary FROM users WHERE id = ?",(user_id,)).fetchall()[0][0]
    cursor_obj.execute(f'UPDATE users SET salary = ? WHERE id = ?', (float(salary)+float(money), user_id))
    connection_obj.commit()
    connection_obj.close()


def exchange_uppdate(exchange):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute(f"UPDATE money SET exchange = '{exchange}'").fetchall()
    connection_obj.commit()
    connection_obj.close()


def application_add(user_id,wallet,money):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("INSERT INTO application (id,wallet,money) VALUES(?,?,?)",
                       (user_id,wallet,money))
    connection_obj.commit()
    connection_obj.close()

def application():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    application = cursor_obj.execute("SELECT * FROM application").fetchall()
    connection_obj.commit()
    connection_obj.close()
    return application

def application_delete(user_id):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DELETE FROM application WHERE id = ?",(user_id,))
    connection_obj.commit()
    connection_obj.close()


def statistics(day,month,year):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    day = len(cursor_obj.execute(f"SELECT * FROM users WHERE ref != 'NULL' AND day = '{day}' AND month = '{month}' AND year = '{year}'").fetchall())
    month = len(cursor_obj.execute(f"SELECT * FROM users WHERE ref != 'NULL' AND month = '{month}' AND year = '{year}'").fetchall())
    year = len(cursor_obj.execute(f"SELECT * FROM users WHERE ref != 'NULL' AND year = '{year}'").fetchall())
    connection_obj.commit()
    connection_obj.close()
    return day,month,year


def add_channel(channels):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    cursor_obj.execute("DELETE FROM channels").fetchall()
    for channel in channels.split(' '):
        try:
            id = channel.split(":")[2]
            channele = ":".join(channel.split(":")[:2])
            cursor_obj.execute(f'INSERT INTO channels (channel, id) VALUES (?, ?)',(channele,id))
            connection_obj.commit()

        except:
            id = None
            channele = channel
            cursor_obj.execute("INSERT INTO channels (channel,id) VALUES(?,?)", (channele, id))
            connection_obj.commit()
    connection_obj.close()

def channels():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = cursor_obj.execute("SELECT channel,id FROM channels").fetchall()
    connection_obj.commit()
    connection_obj.close()
    return text

def add_beta(user_id,ref_id):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    try:
        cursor_obj.execute("INSERT INTO beta (user_id,ref_id) VALUES(?,?)",
                           (user_id,ref_id))
    except:
        pass
    connection_obj.commit()
    connection_obj.close()

def beta(id):
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    try:
        user_id,ref_id = cursor_obj.execute(f"SELECT user_id,ref_id FROM beta WHERE user_id == '{id}'").fetchall()[0]
        cursor_obj.execute(f"DELETE FROM beta WHERE user_id == '{id}'")
        connection_obj.commit()
        connection_obj.close()
        return user_id,ref_id
    except:
        connection_obj.commit()
        connection_obj.close()
        return

def ref():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    text = bool(cursor_obj.execute("SELECT ref FROM Ref").fetchall()[0][0])
    connection_obj.commit()
    connection_obj.close()
    return text

def change_ref():
    connection_obj = sqlite3.connect('DB.db', check_same_thread=False)
    cursor_obj = connection_obj.cursor()
    ref = db.ref()
    if ref:
        cursor_obj.execute(f"UPDATE Ref SET ref = False").fetchall()
        connection_obj.commit()
        connection_obj.close()
        ref = False
    elif not ref:
        cursor_obj.execute(f"UPDATE Ref SET ref = True").fetchall()
        ref = True
        connection_obj.commit()
        connection_obj.close()

    return ref



