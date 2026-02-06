from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Data base
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Retornar con el titulo y contenido
    def __repr__(self):
        return f"Card('{self.title}', '{self.content}')"


@app.route('/')
def index():
    return render_template('index.html')


# Create note route
@app.route('/create_note', methods=['GET', 'POST'])
def create_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        card = Card(title=title, content=content)
        db.session.add(card)
        db.session.commit()
        return redirect('/view_notes')
    else:
        error = 'Hubo un error inesperado, intentelo de nuevo.'
        return error


@app.route('/view_notes')
def view_notes():
    cards = Card.query.all()
    return render_template('view_notes.html', cards=cards)
