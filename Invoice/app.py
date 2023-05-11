from flask import Flask, render_template, request, redirect, url_for

from RR import User,Client,Invoice,db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///invoice.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_users():

    admin = User(username='hello', password='hello123', role='admin')
    manager = User(username='manager', password='manager123', role='manager')

    client1 = Client(name='arunkumar',shortname='arun',email='arun@gmail.com')
    client2 = Client(name='mohamed shahim', shortname='mohamed', email='mohamed@gmail.com')

    invoice1 = Invoice(name='arun',list_of_items='lenova',price=50000,total=52500,status='paid',client_id=1)
    invoice2 = Invoice(name='mohamed', list_of_items='hp', price=40000, total=42000, status='unpaid',client_id=2)

    db.session.add(admin)
    db.session.add(manager)
    db.session.add(client1)
    db.session.add(client2)
    db.session.add(invoice1)
    db.session.add(invoice2)

    db.session.commit()
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'manager':
                return redirect(url_for('generate_invoice'))
        else:
            return 'Invalid credentials. Please try again.'
    return render_template('login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    users = User.query.all()
    clients = Client.query.all()
    invoices = Invoice.query.all()
    return render_template('admin_dashboard.html', users=users, clients=clients, invoices=invoices)

@app.route('/generate/invoice', methods=['GET', 'POST'])
def generate_invoice():
    if request.method == 'POST':
        name = request.form['name']
        list_of_items = request.form['list_of_items']
        price = float(request.form['price'])
        total = float(request.form['total'])
        status = request.form['status']
        client_id = request.form['client_id']
        invoice = Invoice(name=name, list_of_items=list_of_items, price=price, total=total, status=status, client_id=client_id)
        db.session.add(invoice)
        db.session.commit()
        return redirect(url_for('view_invoice', invoice_id=invoice.id))

    clients = Client.query.all()
    return render_template('generate_invoice.html', clients=clients)

@app.route('/invoice/<int:invoice_id>')
def view_invoice(invoice_id):
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('view_invoice.html', invoice=invoice)

if __name__ == '__main__':
    app.run(debug=True)