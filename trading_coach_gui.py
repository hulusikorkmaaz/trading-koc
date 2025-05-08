from flask import Flask, render_template
app = Flask(__name__)
@app.route("/")
def index():
    return "index.html"
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os
from tkcalendar import Calendar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TradingCoachGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Forex Trading Mental Koç")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Stil ayarları
        self.setup_styles()
        
        self.trading_journal = []
        self.load_journal()
        
        self.create_widgets()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Helvetica', 10))
        style.configure("TLabel", font=('Helvetica', 10))
        style.configure("Title.TLabel", font=('Helvetica', 16, 'bold'))
        style.configure("Subtitle.TLabel", font=('Helvetica', 12))
        
    def load_journal(self):
        if os.path.exists('trading_journal.json'):
            with open('trading_journal.json', 'r', encoding='utf-8') as f:
                self.trading_journal = json.load(f)
    
    def save_journal(self):
        with open('trading_journal.json', 'w', encoding='utf-8') as f:
            json.dump(self.trading_journal, f, indent=4, ensure_ascii=False)
    
    def create_widgets(self):
        # Ana başlık
        title_label = ttk.Label(
            self.root,
            text="Forex Trading Mental Koçluk Sistemi",
            style="Title.TLabel"
        )
        title_label.pack(pady=20)
        
        # Ana container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Sol panel (Ana menü)
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Ana menü butonları
        menu_buttons = [
            ("İşlem Öncesi Kontrol Listesi", self.show_pre_trade_checklist),
            ("İşlem Sonrası Değerlendirme", self.show_post_trade_analysis),
            ("Trading Journal", self.show_journal),
            ("İstatistikler ve Analiz", self.show_statistics),
            ("Risk Yönetimi Hesaplayıcı", self.show_risk_calculator),
            ("Günlük/Haftalık Hedefler", self.show_goals)
        ]
        
        for text, command in menu_buttons:
            btn = ttk.Button(
                left_panel,
                text=text,
                command=command,
                width=30
            )
            btn.pack(pady=5, padx=10)
        
        # Sağ panel (Özet bilgiler)
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Özet bilgiler
        self.update_summary(right_panel)
    
    def update_summary(self, parent):
        # Özet başlığı
        ttk.Label(
            parent,
            text="Trading Özeti",
            style="Subtitle.TLabel"
        ).pack(pady=10)
        
        # Son işlemler
        if self.trading_journal:
            last_trade = self.trading_journal[-1]
            ttk.Label(
                parent,
                text=f"Son İşlem: {last_trade['pair']} ({last_trade['direction']})"
            ).pack(pady=5)
            ttk.Label(
                parent,
                text=f"Sonuç: {last_trade['result']}"
            ).pack(pady=5)
        
        # İstatistikler
        if self.trading_journal:
            total_trades = len(self.trading_journal)
            winning_trades = sum(1 for trade in self.trading_journal if trade['result'] == 'Kazanç')
            win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
            
            ttk.Label(
                parent,
                text=f"Toplam İşlem: {total_trades}"
            ).pack(pady=5)
            ttk.Label(
                parent,
                text=f"Kazanç Oranı: %{win_rate:.1f}"
            ).pack(pady=5)
    
    def show_pre_trade_checklist(self):
        checklist_window = tk.Toplevel(self.root)
        checklist_window.title("İşlem Öncesi Kontrol Listesi")
        checklist_window.geometry("700x500")
        
        questions = [
            "Piyasa koşulları uygun mu?",
            "Risk yönetimi planınız hazır mı?",
            "Stop loss ve take profit seviyelerinizi belirlediniz mi?",
            "Duygusal durumunuz dengeli mi?",
            "Trading planınıza uygun bir setup görüyor musunuz?",
            "Haber takvimini kontrol ettiniz mi?",
            "Teknik analiz göstergeleri uyumlu mu?",
            "Risk/Ödül oranı uygun mu?"
        ]
        
        answers = []
        for question in questions:
            frame = ttk.Frame(checklist_window)
            frame.pack(pady=10, padx=20, fill='x')
            
            ttk.Label(frame, text=question).pack(side='left')
            var = tk.StringVar(value="Hayır")
            answers.append(var)
            
            ttk.Radiobutton(
                frame,
                text="Evet",
                variable=var,
                value="Evet"
            ).pack(side='right')
            
            ttk.Radiobutton(
                frame,
                text="Hayır",
                variable=var,
                value="Hayır"
            ).pack(side='right')
        
        def check_answers():
            if all(var.get() == "Evet" for var in answers):
                messagebox.showinfo(
                    "Sonuç",
                    "Tüm kontroller tamam! İşleme hazırsınız."
                )
            else:
                messagebox.showwarning(
                    "Dikkat",
                    "Bazı kontroller tamamlanmadı. Lütfen tekrar değerlendirin."
                )
            checklist_window.destroy()
        
        ttk.Button(
            checklist_window,
            text="Kontrolleri Tamamla",
            command=check_answers
        ).pack(pady=20)
    
    def show_post_trade_analysis(self):
        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("İşlem Sonrası Değerlendirme")
        analysis_window.geometry("700x600")
        
        # Form alanları
        form_frame = ttk.Frame(analysis_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Parite
        ttk.Label(form_frame, text="Parite:").pack(pady=5)
        pair_entry = ttk.Entry(form_frame)
        pair_entry.pack(pady=5)
        
        # İşlem Yönü
        ttk.Label(form_frame, text="İşlem Yönü:").pack(pady=5)
        direction_var = tk.StringVar()
        direction_frame = ttk.Frame(form_frame)
        direction_frame.pack(pady=5)
        ttk.Radiobutton(
            direction_frame,
            text="Long",
            variable=direction_var,
            value="Long"
        ).pack(side='left', padx=10)
        ttk.Radiobutton(
            direction_frame,
            text="Short",
            variable=direction_var,
            value="Short"
        ).pack(side='left', padx=10)
        
        # İşlem Sonucu
        ttk.Label(form_frame, text="İşlem Sonucu:").pack(pady=5)
        result_var = tk.StringVar()
        result_frame = ttk.Frame(form_frame)
        result_frame.pack(pady=5)
        ttk.Radiobutton(
            result_frame,
            text="Kazanç",
            variable=result_var,
            value="Kazanç"
        ).pack(side='left', padx=10)
        ttk.Radiobutton(
            result_frame,
            text="Kayıp",
            variable=result_var,
            value="Kayıp"
        ).pack(side='left', padx=10)
        
        # Risk/Ödül Oranı
        ttk.Label(form_frame, text="Risk/Ödül Oranı:").pack(pady=5)
        rr_entry = ttk.Entry(form_frame)
        rr_entry.pack(pady=5)
        
        # Duygusal Durum
        ttk.Label(form_frame, text="Duygusal Durum:").pack(pady=5)
        emotions_text = tk.Text(form_frame, height=3)
        emotions_text.pack(pady=5)
        
        # Öğrenilen Dersler
        ttk.Label(form_frame, text="Öğrenilen Dersler:").pack(pady=5)
        lessons_text = tk.Text(form_frame, height=3)
        lessons_text.pack(pady=5)
        
        def save_analysis():
            trade_data = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "pair": pair_entry.get(),
                "direction": direction_var.get(),
                "result": result_var.get(),
                "risk_reward": rr_entry.get(),
                "emotions": emotions_text.get("1.0", "end-1c"),
                "lessons": lessons_text.get("1.0", "end-1c")
            }
            
            self.trading_journal.append(trade_data)
            self.save_journal()
            self.update_summary(self.root)
            
            messagebox.showinfo("Başarılı", "İşlem kaydınız başarıyla oluşturuldu!")
            analysis_window.destroy()
        
        ttk.Button(
            form_frame,
            text="Kaydet",
            command=save_analysis
        ).pack(pady=20)
    
    def show_journal(self):
        journal_window = tk.Toplevel(self.root)
        journal_window.title("Trading Journal")
        journal_window.geometry("900x700")
        
        if not self.trading_journal:
            ttk.Label(
                journal_window,
                text="Henüz kayıtlı işlem bulunmuyor."
            ).pack(pady=20)
            return
        
        # Filtreleme seçenekleri
        filter_frame = ttk.Frame(journal_window)
        filter_frame.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(filter_frame, text="Filtrele:").pack(side=tk.LEFT, padx=5)
        filter_var = tk.StringVar(value="Tümü")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=filter_var,
            values=["Tümü", "Kazanç", "Kayıp"]
        )
        filter_combo.pack(side=tk.LEFT, padx=5)
        
        # Journal görüntüleme alanı
        text_widget = tk.Text(journal_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def update_journal(*args):
            text_widget.delete(1.0, tk.END)
            filter_value = filter_var.get()
            
            for trade in self.trading_journal:
                if filter_value == "Tümü" or trade['result'] == filter_value:
                    text_widget.insert(tk.END, f"""
Tarih: {trade['date']}
Parite: {trade['pair']}
Yön: {trade['direction']}
Sonuç: {trade['result']}
Risk/Ödül: {trade.get('risk_reward', 'N/A')}
Duygusal Durum: {trade['emotions']}
Öğrenilen Dersler: {trade['lessons']}
{'='*50}
""")
        
        filter_var.trace('w', update_journal)
        update_journal()
        
        text_widget.config(state=tk.DISABLED)
    
    def show_statistics(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("İstatistikler ve Analiz")
        stats_window.geometry("800x600")
        
        if not self.trading_journal:
            ttk.Label(
                stats_window,
                text="İstatistik için yeterli veri bulunmuyor."
            ).pack(pady=20)
            return
        
        # Grafik oluşturma
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
        
        # Kazanç/Kayıp dağılımı
        results = [trade['result'] for trade in self.trading_journal]
        win_count = results.count('Kazanç')
        loss_count = results.count('Kayıp')
        
        ax1.pie([win_count, loss_count],
                labels=['Kazanç', 'Kayıp'],
                autopct='%1.1f%%',
                colors=['green', 'red'])
        ax1.set_title('Kazanç/Kayıp Dağılımı')
        
        # Duygusal durum analizi
        emotions = [trade['emotions'] for trade in self.trading_journal]
        emotion_counts = {}
        for emotion in emotions:
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        ax2.bar(emotion_counts.keys(), emotion_counts.values())
        ax2.set_title('Duygusal Durum Analizi')
        plt.xticks(rotation=45)
        
        # Grafiği Tkinter penceresine yerleştirme
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def show_risk_calculator(self):
        calc_window = tk.Toplevel(self.root)
        calc_window.title("Risk Yönetimi Hesaplayıcı")
        calc_window.geometry("600x400")
        
        # Hesap formu
        form_frame = ttk.Frame(calc_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Hesap Bakiyesi ($):").pack(pady=5)
        balance_entry = ttk.Entry(form_frame)
        balance_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Risk Yüzdesi (%):").pack(pady=5)
        risk_entry = ttk.Entry(form_frame)
        risk_entry.pack(pady=5)
        
        ttk.Label(form_frame, text="Stop Loss (Pips):").pack(pady=5)
        sl_entry = ttk.Entry(form_frame)
        sl_entry.pack(pady=5)
        
        def calculate():
            try:
                balance = float(balance_entry.get())
                risk_percent = float(risk_entry.get())
                sl_pips = float(sl_entry.get())
                
                risk_amount = balance * (risk_percent / 100)
                position_size = risk_amount / sl_pips
                
                result_text = f"""
Hesaplanan Risk Miktarı: ${risk_amount:.2f}
Önerilen Pozisyon Büyüklüğü: ${position_size:.2f}
"""
                messagebox.showinfo("Hesaplama Sonucu", result_text)
            except ValueError:
                messagebox.showerror("Hata", "Lütfen geçerli sayısal değerler girin!")
        
        ttk.Button(
            form_frame,
            text="Hesapla",
            command=calculate
        ).pack(pady=20)
    
    def show_goals(self):
        goals_window = tk.Toplevel(self.root)
        goals_window.title("Günlük/Haftalık Hedefler")
        goals_window.geometry("600x500")
        
        # Hedef formu
        form_frame = ttk.Frame(goals_window)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Hedef Türü:").pack(pady=5)
        goal_type = tk.StringVar(value="Günlük")
        ttk.Radiobutton(
            form_frame,
            text="Günlük",
            variable=goal_type,
            value="Günlük"
        ).pack()
        ttk.Radiobutton(
            form_frame,
            text="Haftalık",
            variable=goal_type,
            value="Haftalık"
        ).pack()
        
        ttk.Label(form_frame, text="Hedef Açıklaması:").pack(pady=5)
        goal_text = tk.Text(form_frame, height=3)
        goal_text.pack(pady=5)
        
        ttk.Label(form_frame, text="Hedef Tarihi:").pack(pady=5)
        calendar = Calendar(form_frame, selectmode='day')
        calendar.pack(pady=5)
        
        def save_goal():
            goal_data = {
                "type": goal_type.get(),
                "description": goal_text.get("1.0", "end-1c"),
                "date": calendar.get_date()
            }
            
            if not hasattr(self, 'goals'):
                self.goals = []
            
            self.goals.append(goal_data)
            
            # Goals'ı JSON olarak kaydet
            with open('trading_goals.json', 'w', encoding='utf-8') as f:
                json.dump(self.goals, f, indent=4, ensure_ascii=False)
            
            messagebox.showinfo("Başarılı", "Hedef başarıyla kaydedildi!")
            goals_window.destroy()
        
        ttk.Button(
            form_frame,
            text="Hedefi Kaydet",
            command=save_goal
        ).pack(pady=20)

def main():
    root = tk.Tk()
    app = TradingCoachGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
