from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)


class KeyEvent_TX(Module):
    def __init__(
        self,
        e,
        destination=0,
        redundancy=3,
    ):
        self.e = e
        self.destination = destination % 256
        self.redundancy = redundancy
        self._sent_count = 0

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        if keyboard.matrix_update:
            self.send_espnow(keyboard.matrix_update)

    def process_key(self, keyboard, key, is_pressed, int_coord):
        return key

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return

    @property
    def sent_count(self):
        return self._sent_count

    def increment_count(self):
        self._sent_count += 1
        self._sent_count %= 256

    def send_espnow(self, update):
        data = self.serialize_update(update)
        self.try_send(data)
        for i in range(self.redundancy):
            self.try_send(data)
        self.increment_count()

    def serialize_update(self, update):
        buffer = bytearray(4)
        buffer[0] = self.destination
        buffer[1] = self.sent_count
        buffer[2] = update.key_number
        buffer[3] = update.pressed
        return buffer

    # def checksum(self, update):
    #     checksum = bytes([sum(update) & 0xFF])
    #     return checksum

    def try_send(self, data):
        # workaround for issue #9816
        try:
            self.e.send(data)
        except OSError:
            debug("ESP-NOW Error")
            peers = self.e.peers
            self.e.deinit()
            self.e = espnow.ESPNow()
            for peer in peers:
                self.e.peers.append(peer)
            debug("recovered peers: ", self.e.peers)
