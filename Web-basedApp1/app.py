from flask import Flask, request, render_template, redirect, jsonify
import os
import mysql.connector as mysql

conn = mysql.connect(
    host="localhost",
    user = "root",
    password = "12345678",
    port = 3306,
    database = "my_memo"
)


app = Flask(__name__)
template_folder = os.path.join(os.path.dirname(__file__),"templates")
# template_folder = "C:/Users/5A09-03/Desktop/Web-basedApp1/" + "templates/"
#                 = "C:/Users/5A09-03/Desktop/Web-based/templates"

app.static_folder = 'static'
app.static_url_path = "/static"

@app.route('/', methods=['GET']) #API
def index():
    cur = conn.reconnect()
    sql = "SELECT idmemo, firstname, lastname, email FROM memo"
    cur = conn.cursor()
    cur.execute(sql)
    names = cur.fetchall()

    conn.close()
    return render_template("index.html", names=names)

@app.route('/product', methods=['GET'])
def product():
    item = {
        "Name": "Adidas",
        "Model": "Ultra Boots",
        "Price": 180.00
    }
    return "item"

@app.route('/news/<id>', methods=['GET']) #Path parameters
def news(id):
    return "Topic no. is " + id

@app.route('/profile', methods=['GET'])
def profile():
    name = request.args.get("name")
    age = request.args.get("age")
    email = request.args.get("email")
    return "<B>I am "+ name + "," + age +"years. This is my email:" + email + "</B>"

@app.route('/post-data', methods=['POST'])
def post_data():
    name = request.form.get('name')
    age = request.form.get('age')
    email = request.form.get('email')
    return "<B>I am 555 "+ name + "," + age +"years. This is my email:" + email + "</B>"

@app.route('/adduser', methods=['GET'])
def add_newuser():
    return render_template('add_user.html')

@app.route('/adduser_todb', methods=['POST'])
def adduser_todb():
    cur = conn.reconnect()

    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    
    sql = "INSERT INTO memo(firstname, lastname, email)"
    sql += " VALUES(%s,%s,%s)"
    data = (firstname,lastname,email)

    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<idmemo>', methods=["GET"])
def delete(idmemo):
    cur = conn.reconnect()
    sql = "DELETE FROM memo WHERE idmemo=%s"
    data = (idmemo,)

    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<idmemo>', methods=['GET'])
def edit(idmemo):
    cur = conn.reconnect()
    sql = "SELECT idmemo, firstname, lastname, email "
    sql += " FROM memo WHERE idmemo=%s"
    data = (idmemo,)

    cur = conn.cursor()
    cur.execute(sql,data)
    name = cur.fetchone()
    conn.close()
    return render_template('edit_user.html', name=name)

    #return firstname + lastname + email

@app.route('/edituser_todb', methods=["POST"])
def edituser_todb():
    cur = conn.reconnect()

    idmemo = request.form.get('idmemo')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    
    sql = "UPDATE memo SET firstname=%s, lastname=%s, email=%s "
    sql += " WHERE idmemo=%s"
    data = (firstname,lastname,email,idmemo)

    cur = conn.cursor()
    cur.execute(sql,data)
    conn.commit()
    conn.close()
    return redirect('/')

# RESTAPIs
@app.route('/getuser/v1/<idmemo>', methods=["GET"])
def get_user(idmemo):
    cur = conn.reconnect()

    sql = "SELECT idmemo, firstname, lastname, email "
    sql += " FROM memo WHERE idmemo=%s ORDER By firstname"
    data = (idmemo,)
    cur = conn.cursor()
    cur.execute(sql, data)
    records = cur.fetchone()
    conn.close()
    return jsonify(records)

@app.route('/getuser', methods=["GET"])
def get_user_all():
    cur = conn.reconnect()

    sql = "SELECT idmemo, firstname, lastname, email "
    sql += " FROM memo ORDER By firstname"
   
    cur = conn.cursor()
    cur.execute(sql)
    records = cur.fetchall()
    conn.close()
    return jsonify(records)

@app.route('/postuser', methods=["POST"])
def post_user():
    response = request.get_json()
    firstname = response['firstname']
    lastname = response['lastname']
    email = response['email']

    cur = conn.reconnection()
    cur = conn.cursor()
    sql = "INSERT INTO memo(firstname, lastname, email) "
    sql += " VALUES(%s, %s, %s)"
    data = (firstname, lastname, email)
    cur.execute(sql, data)
    conn.commit()
    conn.close()
    return redirect('/getuser')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)