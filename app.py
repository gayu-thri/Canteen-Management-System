from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os

student = {}
admin = {}
teachers = {}

'''
creds = {
    'gayu@gmail.com' : '1122',
    'juju@gmail.com' : '26308'
'''

student['admin'] = 'password'
teachers['admin'] = 'password'
admin['admin'] = 'password'

cart = {}
cart['admin'] = []

app = Flask(__name__)
global user1
user1 = None

@app.route('/')
def home():
    return render_template('logreg.html')
'''
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "You have already logged in... <a href='/logout'>Logout</a>"
'''

@app.route('/home',methods=["POST"])
def logreg():
    if request.form['submit_button']== 'Log in':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return "Already Logged in!"
    elif request.form['submit_button'] == 'Register':
        return render_template('register.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    global user1
    if request.form['choice'] == 'student':
        if request.form['username'] in student and student[request.form['username']] == request.form['password']:
            user1 = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return redirect('/loggedin_student')
    elif request.form['choice'] == 'teacher':
        if request.form['username'] in teachers and teachers[request.form['username']] == request.form['password']:
            user1 = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return redirect('/loggedin_teacher')
    elif request.form['choice'] == 'admin':
        if request.form['username'] in admin and admin[request.form['username']] == request.form['password']:
            user1 = request.form['username']
            session['logged_in'] = True
        else:
            return redirect('/error')
        return redirect('/loggedin_admin')

@app.route('/register',methods=["POST"])
def reg():
    user  = request.form['username']
    pwd = request.form['password']
    if len(pwd) <=6 :
        return "Password should be atleast 7 characters"
    num = 0
    for a in pwd:
        if a>='0' and a<='9':
            num=1
    if num == 0:
        return "Password should have atleast one number"
    alp = 0
    for a in user:
        if (a>='a' and a<='z') or (a>='A' and a<='Z'):
            alp+=1
    if alp != len(user):
        return "Username shoudl have only alphabets"
    if request.form['choice'] == 'teacher':
        teachers[request.form['username']] = request.form['password']
    elif request.form['choice'] == 'student':
        global cart
        cart[request.form['username']] = []
        student[request.form['username']] = request.form['password']
    else:
        admin[request.form['username']] = request.form['password']
    return redirect('/')

@app.route('/loggedin_admin')
def loggedin_admin():
    return render_template('homenew_admin.html')

@app.route('/loggedin_teacher')
def loggedin_teacher():
    return render_template('homenew_teacher.html')

@app.route('/loggedin_student')
def loggedin_student():
    return render_template('homenew_student.html')

@app.route('/homenew_admin',methods = ["POST"])
def homenew_admin():
    if request.form['submit_button'] == 'Log out':
        session['logged_in'] = False
        global user1
        user1 = None
        return redirect('/')

@app.route('/homenew_teacher',methods = ["POST"])
def homenew_teacher():
    if request.form['submit_button'] == 'Log out':
        session['logged_in'] = False
        global user1
        user1 = None
        return redirect('/')

@app.route('/homenew_student',methods = ["POST"])
def homenew_student():
    
    global user1
    global cart
    if request.form['submit_button'] == 'Log out':
        session['logged_in'] = False
        
        user1 = None
        return redirect('/')
    elif request.form['submit_button'] == 'Add to Cart':
        print(cart)
        if 'choice1' in request.form and ('Dosa' in cart[user1]) == False:
            cart[user1].append('Dosa')
        if 'choice2' in request.form and ('Vada' in cart[user1]) == False:
            cart[user1].append('Vada')
        if 'choice3' in request.form and ('Idli' in cart[user1]) == False:
            cart[user1].append('Idli')
        return render_template('homenew_student.html')
    else:
        return redirect('/viewcart')

@app.route('/error')
def err():
    return "Wrong Password"

@app.route('/viewcart')
def viewcart():
    global user1
    s = "Items:\n"
    for ch in cart[user1]:
        s = s+ch+"\n"
    return s

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=4000)