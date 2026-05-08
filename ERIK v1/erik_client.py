import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import socket
import os

SOCKET_PATH = "/tmp/erik.sock"

def send_to_erik(text):
    if not text or not text.strip():
        return
        
    try:
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(SOCKET_PATH)
        client.sendall(text.encode("utf-8"))
        client.close()
    except Exception as e:
        print(f"Error connecting to ERIK: {e}")

class ErikInputDialog(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Chat with ERIK")
        self.set_border_width(10)
        self.set_default_size(400, 100)
        self.set_position(Gtk.WindowPosition.CENTER)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.label = Gtk.Label(label="Type something for ERIK:")
        vbox.pack_start(self.label, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_activates_default(True)
        self.entry.connect("activate", self.on_entry_activate)
        vbox.pack_start(self.entry, True, True, 0)

        self.button = Gtk.Button(label="Send")
        self.button.connect("clicked", self.on_entry_activate)
        vbox.pack_start(self.button, True, True, 0)
        
        self.connect("destroy", Gtk.main_quit)
        self.entry.grab_focus()

    def on_entry_activate(self, widget):
        text = self.entry.get_text()
        send_to_erik(text)
        Gtk.main_quit()

def main():
    win = ErikInputDialog()
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    # Also support command line argument directly
    if len(os.sys.argv) > 1:
        send_to_erik(" ".join(os.sys.argv[1:]))
    else:
        main()
