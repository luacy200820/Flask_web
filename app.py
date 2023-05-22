from flask import Flask, render_template,url_for,request,session,redirect
import sqlite3 
from prettytable import PrettyTable
app = Flask(__name__,static_folder='./templates/')
app.secret_key = 'itissecectkey'
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/delete',methods = ["POST","GET"])
def delete():
    conn = sqlite3.connect("database.db") 
    cur = conn.cursor()
    cur.execute("DELETE from user")
    conn.commit()
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/addrec',methods = ["POST","GET"])
def addrec():
    if request.method == "POST":
        try :
            ID = request.form["username"]
            sec = request.form["password"]


            with sqlite3.connect("database.db") as conn:
                cur= conn.cursor()
                cur.execute("INSERT INTO user (ID,num,eschar,slough,granulation) VALUES (?,?,?,?,?)", (ID,sec,0,0,0))
                conn.commit()
                msg = "successfully add"
        except:
            conn.rollback()
            msg = "error in insert"
        finally:
            conn.close()
            return render_template("result.html",msg=msg)
            

@app.route('/login',methods = ["POST","GET"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        ID = request.form["username"]
        sec = request.form["password"]
        print(ID,sec)

        conn = sqlite3.connect("database.db") 
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM user WHERE ID = ? AND num = ?',(ID,sec))

        acc = cur.fetchone()
        if acc:
            session['loggedin'] = True
            session['id']  = acc['ID']
            session['sec'] = acc['num']
            msg = 'logged in successfully'
            print("acc", acc['ID'])
            return redirect('/analysis')
            # return render_template('analysis.html',msg=acc['num'])
        else:
            msg = 'incorrect id / password'
        # msg = rows
    return render_template('login.html',msg = msg)   
         
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('sec', None)
    return redirect(url_for('login'))


@app.route('/list')
def list():
    conn = sqlite3.connect("database.db") 
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from user")
    rows = cur.fetchall()
 
    return render_template('list.html',rows=rows)
@app.route('/analysis', methods=['GET', 'POST'])
def result():
    selected_date = "NA"
    if request.method == 'POST':
        selected_date = request.form['date']
    value = session['id']   
    n = 0.6
    s = 8
    g = 3
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    query = "UPDATE user SET eschar =?, slough=?,granulation=? WHERE id = ?"
    cursor.execute(query,(n,s,g,value))
    conn.commit()
    # conn.close()
    # query = "SELECT * FROM user"
    # cursor.execute(query)
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row[0])
    #     print(row[1])
    #     print(row[2])
    # print(rows)
    cursor.close()
    conn.close()

    return render_template("analysis.html",value = value,date=selected_date)

if __name__ == '__main__':
   app.run(debug = True)
