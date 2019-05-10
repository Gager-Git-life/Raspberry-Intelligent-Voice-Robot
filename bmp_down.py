import socket
import struct
import threading
import cairo
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GdkPixbuf



class NetworkThread(threading.Thread):
    def __init__(self, app):
        self.app = app
        self.running = True
        super(NetworkThread, self).__init__()

    def run(self):
        header_pattern = 'BII'
        header_size = struct.calcsize(header_pattern)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.settimeout(1)
        sock.bind(('', 3333))
        while self.running:
            try:
                data = sock.recv(1460)
            except socket.timeout:
                continue
            header = struct.unpack_from(header_pattern, data)
            frame, offset, image_size = header

            self.app.set_image_data(offset, data[header_size:])



class MyApp(object):
    """Double buffer in PyGObject with cairo"""

    def __init__(self):
        # Build GUI
        self.window = Gtk.Window()
        self.drawing_area = Gtk.DrawingArea(visible=True, can_focus=False)
        self.window.add(self.drawing_area)

        # Create buffer
        self.double_buffer = None

        # Connect signals
        self.window.connect('destroy', self.main_quit)
        self.drawing_area.connect('configure_event', self.on_configure)
        self.drawing_area.connect('draw', self.on_draw)

        # Everything is ready
        self.window.show()

    def set_image_data(self, offset, data):
        """Draw something into the buffer"""
        if not self.double_buffer:
            return

        # view = self.double_buffer.get_data()
        self.view[offset:offset+len(data)] = data
        self.drawing_area.queue_draw_area(0, 0, 160, 120)

    def main_quit(self, widget):
        """Quit Gtk"""
        Gtk.main_quit()

    def on_draw(self, widget, cr):
        """Throw double buffer into widget drawable"""
        if self.double_buffer is not None:
            cr.set_source_surface(self.double_buffer, 0.0, 0.0)
            cr.paint()
        # else:
        #     print('Invalid double buffer')

        return False

    def on_configure(self, widget, event, data=None):
        """Configure the double buffer based on size of the widget"""

        # Destroy previous buffer
        if self.double_buffer is not None:
            # self.double_buffer.finish()
            # self.double_buffer = None
            return

        # Create a new buffer
        self.view_data = bytearray(160*120*2)
        self.view = memoryview(self.view_data)
        self.double_buffer = cairo.ImageSurface.create_for_data(
            self.view,
            cairo.FORMAT_RGB16_565,
            160,
            120
        )

        # self.double_buffer.set_device_scale(0.5, 0.5)

        return False

if __name__ == '__main__':
    gui = MyApp()
    thread = NetworkThread(gui)
    thread.start()
    Gtk.main()
    thread.running = False
