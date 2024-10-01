from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja bazy danych SQLite dla lokalnych testów
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletter.db'  # Lokalna baza SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model bazy danych
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Strona główna
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        if email:
            try:
                # Tworzymy nowego subskrybenta
                new_subscriber = Subscriber(email=email)
                db.session.add(new_subscriber)
                db.session.commit()  # Zapisujemy do bazy danych
            except Exception as e:
                print(f"Problem z zapisem: {e}")
            return redirect("/")
    return render_template("index.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Tworzymy tabele w lokalnej bazie SQLite, jeśli nie istnieją
    app.run(debug=True)
