import socket
import threading
import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

# App ka background color (Dark Theme)
Window.clearcolor = (0.05, 0.05, 0.1, 1)

class NetShareApp(App):
    def build(self):
        self.title = "NetShare P2P - Private Bridge"
        
        # Main Layout
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        # Header
        layout.add_widget(Label(
            text="NetShare P2P", 
            font_size='35sp', 
            bold=True, 
            color=(0, 0.8, 1, 1),
            size_hint_y=None,
            height=100
        ))

        # IP Input Box
        self.ip_input = TextInput(
            hint_text="Dost ka Tailscale IP yahan dalein",
            multiline=False,
            size_hint_y=None,
            height=100,
            padding_y=(20, 20),
            background_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.ip_input)

        # Start Server Button (For the Friend)
        self.server_btn = Button(
            text="START SERVER (Data Denewala)",
            background_color=(0.1, 0.7, 0.3, 1),
            bold=True,
            size_hint_y=None,
            height=120
        )
        self.server_btn.bind(on_press=self.start_server_thread)
        layout.add_widget(self.server_btn)

        # Connect Button (For the User)
        self.connect_btn = Button(
            text="CONNECT (Data Lenewala)",
            background_color=(0.1, 0.4, 0.9, 1),
            bold=True,
            size_hint_y=None,
            height=120
        )
        self.connect_btn.bind(on_press=self.start_client_thread)
        layout.add_widget(self.connect_btn)

        # Status Label
        self.status = Label(
            text="Status: Taiyar (Offline)",
            font_size='16sp',
            color=(0.8, 0.8, 0.8, 1)
        )
        layout.add_widget(self.status)

        return layout

    # UI update karne ka tareeka
    def update_status(self, msg):
        self.status.text = f"Status: {msg}"

    # --- SERVER LOGIC (Dost ka kaam) ---
    def start_server_thread(self, instance):
        threading.Thread(target=self.run_server, daemon=True).start()

    def run_server(self):
        Clock.schedule_once(lambda dt: self.update_status("Server: Checking Internet..."))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('0.0.0.0', 9999)) # Port 9999 use kar rahe hain
            s.listen(1)
            Clock.schedule_once(lambda dt: self.update_status("Server: Waiting for Friend..."))
            
            conn, addr = s.accept()
            Clock.schedule_once(lambda dt: self.update_status(f"Connected to: {addr[0]}"))

            while True:
                # Client se website request receive karna
                request_url = conn.recv(1024).decode()
                if not request_url: break
                
                # Proxy Logic: Dost ke net se data lana
                try:
                    response = urllib.request.urlopen(request_url).read()
                    conn.sendall(response)
                except:
                    conn.sendall(b"Error: Could not fetch data.")
            conn.close()
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status(f"Server Error: {str(e)}"))

    # --- CLIENT LOGIC (Aapka kaam) ---
    def start_client_thread(self, instance):
        threading.Thread(target=self.run_client, daemon=True).start()

    def run_client(self):
        target_ip = self.ip_input.text
        if not target_ip:
            Clock.schedule_once(lambda dt: self.update_status("Error: IP Address empty!"))
            return

        try:
            Clock.schedule_once(lambda dt: self.update_status(f"Connecting to {target_ip}..."))
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(15)
            s.connect((target_ip, 9999))
            
            # Test request bhejna
            test_url = "http://www.google.com"
            s.send(test_url.encode())
            
            # Dost ke net se data receive karna
            data = s.recv(4096)
            if data:
                Clock.schedule_once(lambda dt: self.update_status("Success! Dost ka Net chal raha hai."))
            s.close()
        except Exception as e:
            Clock.schedule_once(lambda dt: self.update_status("Connection Failed!"))

if __name__ == "__main__":
    NetShareApp().run()
