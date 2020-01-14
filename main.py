from flask import *
import mysql.connector
import os
from werkzeug.utils import secure_filename
	
app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def createCinnect():
	conn = mysql.connector.connect(host='cloud-final-db.cuuzvwa8vpbk.us-east-1.rds.amazonaws.com',
		user='admin', password='s1051534', database='cloudFinalDB')
	return conn
	
def getLoginDetails(): #OK
	conn = createCinnect()
	cur = conn.cursor()
	
	if 'email' not in session:
		loggedIn = False
		name = ''
		noOfItems = 0
	else:
		loggedIn = True
		
		sql = 'SELECT userId, name FROM users WHERE email = %s'
		adr = (session['email'], )
		cur.execute(sql, adr)
		
		userId, name = cur.fetchone()

		sql = 'SELECT count(productId) FROM kart WHERE userId = %s'
		adr = (userId, )
		cur.execute(sql, adr)		

		noOfItems = cur.fetchone()[0]
	conn.close()
	return (loggedIn, name, noOfItems)

@app.route("/")#OK
def root():
	loggedIn, name, noOfItems = getLoginDetails()

	conn = createCinnect()
	cur = conn.cursor()
	
	cur.execute('SELECT productId, name, price, description, image, stock FROM products')
	itemData = cur.fetchall()
	cur.execute('SELECT categoryId, name FROM categories')
	categoryData = cur.fetchall()
			
	itemData = parse(itemData)   
	return render_template('home.html', itemData=itemData, loggedIn=loggedIn, name=name, noOfItems=noOfItems, categoryData=categoryData)

@app.route("/add") #上架商品
def admin():
	conn = createCinnect()
	cur = conn.cursor()
	cur.execute("SELECT categoryId, name FROM categories")
	categories = cur.fetchall()
	conn.close()
	return render_template('add.html', categories=categories)

@app.route("/addItem", methods=["GET", "POST"]) #沒有這網頁，應該是和route("/add")搭配寫
def addItem():
	if request.method == "POST":
		name = request.form['name']
		price = float(request.form['price'])
		description = request.form['description']
		stock = int(request.form['stock'])
		categoryId = int(request.form['category'])

		#Uploading image procedure
		image = request.files['image']
		if image and allowed_file(image.filename):
			filename = secure_filename(image.filename)
			image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		imagename = filename
		
		conn = mysql.connector.connect(
			host='cloud-final-db.cuuzvwa8vpbk.us-east-1.rds.amazonaws.com',
			user='admin',
			password='s1051534',
			database='cloudFinalDB')
		
		try:
			cur = conn.cursor()
			
			sql = 'INSERT INTO products (name, price, description, image, stock, categoryId) VALUES (%s, %s, %s, %s, %s, %s)'
			adr = (name, price, description, imagename, stock, categoryId)
			cur.execute(sql, adr)
			
			conn.commit()
			msg="added successfully"
		except:
			msg="error occured"
			conn.rollback()
		conn.close()
		print(msg)
		return redirect(url_for('root'))

@app.route("/remove") #下架商品
def remove():
	conn = createCinnect()
	cur = conn.cursor()
	cur.execute('SELECT productId, name, price, description, image, stock FROM products')
	data = cur.fetchall()
	conn.close()
	return render_template('remove.html', data=data)

@app.route("/removeItem") #沒有這網頁，應該是和route("/remove")搭配寫
def removeItem():
	productId = request.args.get('productId')
	
	conn = createCinnect()
	try:
		cur = conn.cursor()
		
		sql = 'DELETE FROM products WHERE productID = %s'
		adr = (productId, )
		cur.execute(sql, adr)
		
		conn.commit()
		msg = "Deleted successsfully"
	except:
		conn.rollback()
		msg = "Error occured"
	conn.close()
	print(msg)
	return redirect(url_for('root'))

@app.route("/displayCategory") #OK
def displayCategory():
		loggedIn, name, noOfItems = getLoginDetails()
		categoryId = request.args.get("categoryId")
		
		conn = mysql.connector.connect(
			host='cloud-final-db.cuuzvwa8vpbk.us-east-1.rds.amazonaws.com',
			user='admin',
			password='s1051534',
			database='cloudFinalDB')
		
		cur = conn.cursor()
		
		sql = "SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = %s"
		adr = (categoryId, )
		cur.execute(sql, adr)
		
		data = cur.fetchall()
		conn.close()
		categoryName = data[0][4]
		data = parse(data)
		return render_template('displayCategory.html', data=data, loggedIn=loggedIn, name=name, noOfItems=noOfItems, categoryName=categoryName)

@app.route("/account/profile")
def profileHome():
	if 'email' not in session:
		return redirect(url_for('root'))
	loggedIn, name, noOfItems = getLoginDetails()
	return render_template("profileHome.html", loggedIn=loggedIn, name=name, noOfItems=noOfItems)

@app.route("/account/profile/view")
def viewProfile():
	if 'email' not in session:
		return redirect(url_for('root'))
	loggedIn, name, noOfItems = getLoginDetails()
	conn = createCinnect()
	cur = conn.cursor()
	
	sql = 'SELECT userId, email, name, phone FROM users WHERE email = %s'
	adr = (session['email'], )
	cur.execute(sql, adr)
	
	profileData = cur.fetchone()
	conn.close()
	return render_template("viewProfile.html", profileData=profileData, loggedIn=loggedIn, name=name, noOfItems=noOfItems)
	
@app.route("/account/profile/edit")
def editProfile():
	if 'email' not in session:
		return redirect(url_for('root'))
	loggedIn, name, noOfItems = getLoginDetails()
	conn = createCinnect()
	cur = conn.cursor()
	
	sql = 'SELECT userId, email, name, phone FROM users WHERE email = %s'
	adr = (session['email'], )
	cur.execute(sql, adr)
	
	profileData = cur.fetchone()
	conn.close()
	return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, name=name, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	loggedIn, name, noOfItems = getLoginDetails()
	if request.method == "POST":
		oldPassword = request.form['oldpassword']
		newPassword = request.form['newpassword']

		conn = createCinnect()
		cur = conn.cursor()
		
		sql = 'SELECT userId, password FROM users WHERE email = %s'
		adr = (session['email'], )
		cur.execute(sql, adr)
		
		userId, password = cur.fetchone()
		if (password == oldPassword):
			try:
				sql = 'UPDATE users SET password = %s WHERE userId = %s'
				adr = (newPassword, userId)
				cur.execute(sql, adr)
				
				conn.commit()
				msg="Changed successfully"
			except:
				conn.rollback()
				msg = "Failed"
			return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, name=name, noOfItems=noOfItems)
		else:
			msg = "Wrong password"
		conn.close()
		return render_template("changePassword.html", msg=msg, loggedIn=loggedIn, name=name, noOfItems=noOfItems)
	else:
		return render_template("changePassword.html", loggedIn=loggedIn, name=name, noOfItems=noOfItems)

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
	if request.method == 'POST':
		email = request.form['email']
		name = request.form['name']
		phone = request.form['phone']
		conn = createCinnect()
		try:
			cur = conn.cursor()
			sql = 'UPDATE users SET name = %s, phone = %s WHERE email = %s'
			adr = (name, phone, email)
			cur.execute(sql, adr)

			conn.commit()
			msg = "Saved Successfully"
		except:
			conn.rollback()
			msg = "Error occured"
		conn.close()
		return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
	if 'email' in session:
		return redirect(url_for('root'))
	else:
		return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if is_valid(email, password):
			session['email'] = email
			return redirect(url_for('root'))
		else:
			error = 'Invalid UserId / Password'
			return render_template('login.html', error=error)

@app.route("/productDescription") # OK
def productDescription():
	loggedIn, name, noOfItems = getLoginDetails()
	productId = request.args.get('productId')
	conn = createCinnect()
	cur = conn.cursor()
	
	sql = 'SELECT productId, name, price, description, image, stock FROM products WHERE productId = %s'
	adr = (productId, )
	cur.execute(sql, adr)
	
	productData = cur.fetchone()
	conn.close()
	return render_template("productDescription.html", data=productData, loggedIn = loggedIn, name = name, noOfItems = noOfItems)

@app.route("/addToCart")
def addToCart():
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	else:
		productId = int(request.args.get('productId'))
		conn = createCinnect()
		cur = conn.cursor()
		
		sql = 'SELECT userId FROM users WHERE email = %s'
		adr = (session['email'], )
		cur.execute(sql, adr)
		
		userId = cur.fetchone()[0]
		try:
			sql = 'INSERT INTO kart (userId, productId) VALUES (%s, %s)'
			adr = (userId, productId)
			cur.execute(sql, adr)
			conn.commit()
			msg = "Added successfully"
		except:
			conn.rollback()
			msg = "Error occured"
		conn.close()
		return redirect(url_for('root'))

@app.route("/account/orders")
def yourOrders():
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	loggedIn, name, noOfItems = getLoginDetails()
	email = session['email']
	conn = createCinnect()
	cur = conn.cursor()

	sql = 'SELECT userId FROM users WHERE email = %s'
	adr = (email,)
	cur.execute(sql, adr)

	userId = cur.fetchone()[0]

	sql = 'SELECT * FROM history WHERE userId = %s'
	adr = (userId,)
	cur.execute(sql, adr)

	orderHistory = cur.fetchall()
	products = []
	for row in orderHistory:
		totalPrice = 0
		items = row[4].split('+')
		detail = []

		for item in items:
			tmp = item.split('^')
			detail.append('%05d %s - %s' % (int(tmp[0]), tmp[1], tmp[2]))

			totalPrice += int(tmp[2][1:])

		products.append(['%05d' % row[0], row[1], detail, str(totalPrice)])

	# [訂單編號 時間 (商品編號+明細) $$]

	return render_template("yourOrders.html", products=products, totalPrice=totalPrice, loggedIn=loggedIn, name=name,
						   noOfItems=noOfItems)

@app.route("/cart")
def cart():
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	loggedIn, name, noOfItems = getLoginDetails()
	email = session['email']
	conn = createCinnect()
	cur = conn.cursor()
	
	sql = 'SELECT userId FROM users WHERE email = %s'
	adr = (email, )
	cur.execute(sql, adr)
	
	userId = cur.fetchone()[0]
	
	sql = 'SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = %s'
	adr = (userId, )
	cur.execute(sql, adr)
	
	products = cur.fetchall()
	totalPrice = 0
	for row in products:
		totalPrice += row[2]
	return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, name=name, noOfItems=noOfItems)
	
@app.route("/checkout", methods = ['POST', 'GET'])
def checkout():
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	loggedIn, name, noOfItems = getLoginDetails()
	email = session['email']
	conn = createCinnect()
	cur = conn.cursor()
	
	sql = 'SELECT userId FROM users WHERE email = %s'
	adr = (email, )
	cur.execute(sql, adr)
	
	userId = cur.fetchone()[0]
	
	sql = 'SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = %s'
	adr = (userId, )
	cur.execute(sql, adr)
	
	products = cur.fetchall()
	totalPrice = 0
	for row in products:
		totalPrice += row[2]
		
	if request.method == 'POST':
		pay = request.form['pay']
		detail = request.form['detail']
		# get pay list -> write to history db -> delete user from cart db
		sql = 'SELECT userId FROM users WHERE email = %s'
		adr = (session['email'], )
		cur.execute(sql, adr)
		userId = cur.fetchone()[0]
		
		sql = 'SELECT productId FROM kart WHERE userId = %s'
		adr = (userId, )
		cur.execute(sql, adr)
		productIds = cur.fetchall()
		
		detailList = [] #(name, pid)
		for i in productIds:	
			sql = 'SELECT name, price From products WHERE productId = %s'
			adr = i
			cur.execute(sql, adr)
			detailList.append(cur.fetchone())
		
		try:
			# write to history db
			detail = ''
			listNum = ''
			for i,j in enumerate(detailList):
				detail += str(productIds[i][0]) + '^' + detailList[i][0] + '^$' + str(detailList[i][1]) + '+'
				listNum += str(productIds[i][0]) + '+'
			detail = detail[:-1]
			listNum = listNum[:-1]

			sql = 'INSERT INTO history (date, userId, status, detail, listNum) VALUES (now(), %s, %s, %s, %s)'
			adr = [userId, '3', detail, listNum]	
			cur.execute(sql, adr)
			conn.commit()

			# delete user from cart db
			sql = 'DELETE FROM kart WHERE userId = %s'
			adr = (userId, )
			print('*******')
			cur.execute(sql, adr)
			conn.commit()
			checkresponse = "Successful transaction!"
			noOfItems = 0
		except:
			checkresponse = "transaction failed"
		conn.close()
		return render_template("checkoutResponse.html", checkresponse = checkresponse, loggedIn=loggedIn, name=name, noOfItems=noOfItems)
		
	return render_template("checkout.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, name=name, noOfItems=noOfItems)

@app.route("/removeFromCart")
def removeFromCart():
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	email = session['email']
	productId = int(request.args.get('productId'))
	conn = createCinnect()
	cur = conn.cursor()
	
	sql = 'SELECT userId FROM users WHERE email = %s'
	adr = (email, )
	cur.execute(sql, adr)
	
	userId = cur.fetchone()[0]
	try:
		sql = 'DELETE FROM kart WHERE userId = %s AND productId = %s LIMIT 1'
		adr = (userId, productId)
		cur.execute(sql, adr)
		
		conn.commit()
		msg = "removed successfully"
	except:
		conn.rollback()
		msg = "error occured"
	conn.close()
	return redirect(url_for('cart'))

@app.route("/removeFromCheckout")
def removeFromCheckout():
	if 'email' not in session:
		return redirect(url_for('loginForm'))
	email = session['email']
	productId = int(request.args.get('productId'))
	conn = createCinnect()
	cur = conn.cursor()
	
	sql = 'SELECT userId FROM users WHERE email = %s'
	adr = (email, )
	cur.execute(sql, adr)
	
	userId = cur.fetchone()[0]
	try:
		sql = 'DELETE FROM kart WHERE userId = %s AND productId = %s LIMIT 1'
		adr = (userId, productId)
		cur.execute(sql, adr)
		
		conn.commit()
		msg = "removed successfully"
	except:
		conn.rollback()
		msg = "error occured"
	conn.close()
	return redirect(url_for('checkout'))

@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('root'))

def is_valid(email, password):
	conn = createCinnect()
	cur = conn.cursor()
	cur.execute('SELECT email, password FROM users')
	data = cur.fetchall()
	for row in data:
		if row[0] == email and row[1] == password:
			return True
	return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
	if request.method == 'POST':
		#Parse form data	
		email = request.form['email']
		password = request.form['password']
		cpassword = request.form['cpassword']
		name = request.form['name']
		phone = request.form['phone']

		conn = createCinnect()
		try:
			cur = conn.cursor()
			
			sql = 'INSERT INTO users (email, password, name, phone) VALUES (%s, %s, %s, %s)'
			adr = (email, password, name, phone)
			cur.execute(sql, adr)
		
			conn.commit()

			msg = "Registered Successfully"
		except:
			conn.rollback()
			msg = "Error occured"
		conn.close()
		return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
	return render_template("register.html")

def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
	ans = []
	i = 0
	while i < len(data):
		curr = []
		for j in range(7):
			if i >= len(data):
				break
			curr.append(data[i])
			i += 1
		ans.append(curr)
	return ans

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, debug=True)
