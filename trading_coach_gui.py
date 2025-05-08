from flask import Flask, request, jsonify, render_template
from models import db, PreTradeChecklist, PostTradeAnalysis
import os

app = Flask(__name__)

# Veritabanı konfigürasyonu
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'trades.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Veritabanını başlat
db.init_app(app)

# Veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pre-trade-checklist')
def pre_trade_checklist_page():
    return render_template('pre_trade_checklist.html')

@app.route('/post-trade-analysis')
def post_trade_analysis_page():
    return render_template('post_trade_analysis.html')

@app.route('/journal')
def journal():
    analyses = PostTradeAnalysis.query.order_by(PostTradeAnalysis.created_at.desc()).all()
    return render_template('journal.html', analyses=analyses)

@app.route('/pre-trade-checklist', methods=['POST'])
def pre_trade_checklist():
    try:
        data = request.get_json()
        
        checklist = PreTradeChecklist(
            market_conditions=bool(data.get('market_conditions')),
            market_trend=bool(data.get('market_trend')),
            support_resistance=bool(data.get('support_resistance')),
            price_zone=bool(data.get('price_zone')),
            mitigation=bool(data.get('mitigation')),
            fvg=bool(data.get('fvg')),
            opposing_force=bool(data.get('opposing_force')),
            emotional_state=bool(data.get('emotional_state')),
            risk_tolerance=bool(data.get('risk_tolerance')),
            trading_plan=bool(data.get('trading_plan')),
            news_check=bool(data.get('news_check'))
        )
        
        db.session.add(checklist)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in pre-trade-checklist: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/post-trade-analysis', methods=['POST'])
def post_trade_analysis():
    try:
        data = request.get_json()
        
        analysis = PostTradeAnalysis(
            pair=data.get('pair'),
            direction=data.get('direction'),
            entry_price=float(data.get('entry_price', 0)),
            stop_loss=float(data.get('stop_loss', 0)),
            take_profit=float(data.get('take_profit', 0)),
            result=data.get('result'),
            exit_price=float(data.get('exit_price', 0)),
            risk_amount=float(data.get('risk_amount', 0)),
            reward_amount=float(data.get('reward_amount', 0)),
            risk_reward_ratio=float(data.get('risk_reward_ratio', 0)),
            emotions=data.get('emotions'),
            emotional_impact=data.get('emotional_impact'),
            lessons=data.get('lessons'),
            improvements=data.get('improvements')
        )
        
        db.session.add(analysis)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in post-trade-analysis: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/delete-analysis/<int:id>', methods=['POST'])
def delete_analysis(id):
    try:
        analysis = PostTradeAnalysis.query.get_or_404(id)
        db.session.delete(analysis)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error in delete-analysis: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
