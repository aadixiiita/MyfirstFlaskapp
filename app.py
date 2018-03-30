from flask import Flask, render_template, request, redirect, url_for ,flash,session
import pymysql
from flask_session import Session


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'aadi'



@app.route('/')

def home():	
	return render_template('index.html')

@app.route('/blog' ,methods=['GET','POST'])

def blog():		
		
	if request.method == 'POST':
		data1 = request.form['title']
		data2 = request.form['subtitle']
		data3 = request.form['author']
		data4 = request.form['content']
		connection = pymysql.connect(host='localhost' ,user='root' ,password='',db='test')
		
		with connection.cursor() as cursor:	
			cursor.execute('''INSERT INTO blog(title,subheading,author,content) VALUES ( %s ,%s ,%s,%s)''', (data1 ,data2,data3 ,data4) )
			connection.commit()	

	
		connection = pymysql.connect(host='localhost' ,user='root' ,password='',db='test')

		with connection.cursor() as cursor:

			cursor.execute(" SELECT * FROM blog ")
			tup = cursor.fetchall()
			posts = [list(x) for x in tup]
		
			return render_template('blog.html',posts=posts)
			
			
				
				
	else:
		connection = pymysql.connect(host='localhost' ,user='root' ,password='',db='test')

		with connection.cursor() as cursor:

			cursor.execute(" SELECT * FROM blog ")
			tup = cursor.fetchall()
			posts = [list(x) for x in tup]
			
		return render_template('blog.html',posts=posts)

	


@app.route('/posts/<int:post_id>',methods=['GET','POST'])

def posts(post_id):	
	connection = pymysql.connect(host='localhost' ,user='root' ,password='',db='test')
	with connection.cursor() as cursor:	

		data =cursor.execute('''SELECT * FROM blog WHERE post_id = (%s)''', (post_id) )
		data = cursor.fetchone()
		posts= list(data)

	return render_template('posts.html',posts=posts)

@app.route('/add' , methods=['GET','POST'])

def add():	
	return render_template('add.html')

@app.route('/login', methods=['GET','POST'])

def login():	
	return render_template('login.html')

@app.route('/reg', methods=['GET','POST'])

def reg():	
	return render_template('reg.html')

@app.route('/postd', methods=['GET','POST'])

def postd():
	if request.method == 'POST':
		data1 = request.form['user']
		data2 = request.form['pass']
		connection = pymysql.connect(host='localhost' ,user='root' ,password='',db='test')
		with connection.cursor() as cursor:			
			data =cursor.execute('''SELECT * FROM reg WHERE user = (%s)''', (data1) )
			if(int(data)>0):

				data = cursor.fetchone()[3]
				if(data2 == data):		
					
					
					return redirect(url_for('blog'))
				else:
					return "Invalid Credentials"
			else:
				return "Invalid Username"
		
	else:
		return 'NOT Allowed'

@app.route('/postreg', methods=['GET','POST'])

def postreg():
	if request.method == 'POST':
		data1 = request.form['name']
		data2 = request.form['email']
		data3 = request.form['user']
		data4 = request.form['pass']
		connection = pymysql.connect(host='localhost' ,user='root' ,password='',db='test')
		
		with connection.cursor() as cursor:	
			data =cursor.execute('''SELECT * FROM reg WHERE user = (%s)''', (data3) )
			if(int(data)>0):
				return 'Username already exist'
			else:
				cursor.execute('''INSERT INTO reg(name,email,user,pass) VALUES ( %s ,%s ,%s,%s)''', (data1 ,data2,data3 ,data4) )
				connection.commit()	
				flash("Succesfully Registered")
				return redirect(url_for('login'))
		
	else:
		return 'NOT Allowed'

		
@app.route('/index')
def index():
	connection = pymysql.connect(host='localhost' ,user='root' ,password='',db='test')
	with connection.cursor() as cursor:
		cursor.execute(" SELECT * FROM flask ")
		rv = cursor.fetchall()
		return str(rv)

if __name__ == '__main__':

	app.run(debug=True)
