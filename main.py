from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.lang import Builder

from core.terms import require_terms_acceptance
from core.user import load_user, save_user
from utils.btc import usd_to_btc
from donations.qr import generate_qr
from exchanges.manager import ExchangeManager

AGENTS = ["Macro LLM", "Arbitrage", "On-chain Flow", "RL Governor"]

KV = """
BoxLayout:
    orientation: 'vertical'
    Label:
        text: "HoodBot By Anthony Hood Dashboard"
        size_hint_y: 0.1
    BoxLayout:
        id: dashboard
        orientation: 'horizontal'
        size_hint_y: 0.6
        spacing: 5
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.1
        Label:
            text: "Risk:"
        Slider:
            id: risk_slider
            min: 1
            max: 10
            value: 5
            step: 1
        Label:
            id: risk_val
            text: str(int(risk_slider.value))
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.1
        Label:
            text: "Speed:"
        Slider:
            id: speed_slider
            min: 1
            max: 10
            value: 5
            step: 1
        Label:
            id: speed_val
            text: str(int(speed_slider.value))
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.1
        Button:
            text: "Check Donation / BTC QR"
            on_press: app.show_donation_prompt()
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 0.1
        Button:
            text: "Toggle Live/Simulation Mode"
            on_press: app.toggle_mode()
"""

class HoodBot(App):
    def build(self):
        require_terms_acceptance()
        self.user = load_user()
        if not self.user:
            self.user = self.create_new_user()
            save_user(self.user)
        self.mode = self.user.get("mode","simulation")
        self.root = Builder.load_string(KV)
        self.exchange_manager = ExchangeManager(self.user.get("api",{}), self.mode)
        self.agent_labels = []
        for agent in AGENTS:
            lbl = Label(text=f"{agent}: Idle", halign="center")
            self.root.ids.dashboard.add_widget(lbl)
            self.agent_labels.append(lbl)
        Clock.schedule_interval(self.update_dashboard,2)
        self.root.ids.risk_slider.bind(value=self.update_risk_label)
        self.root.ids.speed_slider.bind(value=self.update_speed_label)
        return self.root

    def create_new_user(self):
        print("Welcome to HoodBot!")
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Create password (24 chars recommended): ")
        print("Enter your API keys for live trading:")
        binance_key = input("Binance API Key: ")
        binance_secret = input("Binance Secret: ")
        crypto_key = input("Crypto.com API Key: ")
        crypto_secret = input("Crypto.com Secret: ")
        mode = input("Choose mode [live/simulation]: ").lower()
        if mode not in ["live","simulation"]:
            mode = "simulation"
        return {
            "username": username,
            "email": email,
            "password": password,
            "api": {
                "binance":{"key":binance_key,"secret":binance_secret},
                "crypto":{"key":crypto_key,"secret":crypto_secret}
            },
            "mode": mode
        }

    def toggle_mode(self):
        self.mode = "simulation" if self.mode=="live" else "live"
        self.user["mode"]=self.mode
        save_user(self.user)
        self.exchange_manager.mode = self.mode
        print(f"Mode switched to: {self.mode}")

    def update_risk_label(self, instance, value):
        self.root.ids.risk_val.text = str(int(value))

    def update_speed_label(self, instance, value):
        self.root.ids.speed_val.text = str(int(value))

    def update_dashboard(self, dt):
        for i, lbl in enumerate(self.agent_labels):
            status = random.choice(["Analyzing","Buying","Selling","Idle"])
            profit_est = round(random.uniform(-1.5,3.0),2)
            lbl.text = f"{AGENTS[i]}: {status} | Est Profit: ${profit_est}"

    def show_donation_prompt(self):
        wallet="3Cpuk25wV1bCpwir5YAXXWREEgtawxC62k"
        min_usd=25
        btc_equiv = usd_to_btc(min_usd)
        if btc_equiv:
            generate_qr(wallet)
            print(f"BTC donation QR generated -> {wallet}")
            print(f"Approx BTC: {btc_equiv:.6f}")
        else:
            print("BTC price fetch failed.")

if __name__=="__main__":
    HoodBot().run()
