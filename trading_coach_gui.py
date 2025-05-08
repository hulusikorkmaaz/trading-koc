import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Mutlak veritabanı yolu
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'trades.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Trade modeli
class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pair = db.Column(db.String(50))
    direction = db.Column(db.String(10))
    result = db.Column(db.String(10))
    risk_amount = db.Column(db.Float)
    reward_amount = db.Column(db.Float)
    risk_reward_ratio = db.Column(db.Float)
    emotions = db.Column(db.String(200))
    lessons = db.Column(db.String(200))
    improvements = db.Column(db.String(200))
    date = db.Column(db.String(50))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post-trade-analysis", methods=["GET", "POST"])
def post_trade_analysis():
    if request.method == "POST":
        trade = Trade(
            pair=request.form.get("pair"),
            direction=request.form.get("direction"),
            result=request.form.get("result"),
            risk_amount=request.form.get("risk_amount", type=float),
            reward_amount=request.form.get("reward_amount", type=float),
            risk_reward_ratio=request.form.get("risk_reward_ratio", type=float),
            emotions=request.form.get("emotions"),
            lessons=request.form.get("lessons"),
            improvements=request.form.get("improvements"),
            date=request.form.get("date")
        )
        db.session.add(trade)
        db.session.commit()
        return redirect(url_for("journal"))
    return render_template("post_trade_analysis.html")

@app.route("/journal")
def journal():
    trades = Trade.query.all()
    return render_template("journal.html", trades=trades)

@app.route("/statistics")
def statistics():
    return render_template("statistics.html")

@app.route("/pre-trade-checklist", methods=["GET", "POST"])
def pre_trade_checklist():
    if request.method == "POST":
        # Burada formdan gelen verileri işleyebilirsin
        return redirect(url_for("journal"))
    return render_template("pre_trade_checklist.html")

@app.route("/risk-calculator")
def risk_calculator():
    return render_template("risk_calculator.html")

@app.route("/delete-trade/<int:trade_id>", methods=["POST"])
def delete_trade(trade_id):
    trade = Trade.query.get_or_404(trade_id)
    db.session.delete(trade)
    db.session.commit()
    return redirect(url_for("journal"))

# Render ve diğer production ortamları için: 
# Sadece tabloyu oluştur, sunucuyu başlatma!
db_path = os.path.join(basedir, 'trades.db')
if not os.path.exists(db_path):
    with app.app_context():
        db.create_all()

# Sadece localde çalıştırmak için:
if __name__ == "__main__":
    app.run(debug=True)
