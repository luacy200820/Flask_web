from flask import Flask, render_template,url_for,request,session
import sqlite3 
app = Flask(__name__,static_folder='./templates/')
app.secret_key = 'itissecectkey'
@app.route('/')
def home():
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
                cur.execute("INSERT INTO user (ID,num) VALUES (?,?)", (ID,sec))
                conn.commit()
                msg = "successfully add"
        except:
            conn.rollback()
            msg = "error in insert"
        finally:
            return render_template("result.html",msg=msg)
            conn.close()

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
            return render_template('analysis.html',msg=msg)
        else:
            msg = 'incorrect id / password'
        # msg = rows
    return render_template('login.html',msg = msg)   


@app.route('/list')
def list():
    conn = sqlite3.connect("database.db") 
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("select * from user")
    rows = cur.fetchall()
    return render_template('list.html',rows=rows)
if __name__ == '__main__':
   app.run(debug = True)
