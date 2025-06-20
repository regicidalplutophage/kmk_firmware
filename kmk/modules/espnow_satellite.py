from kmk.modules import Module


class ESPNOW_Satellite(Module):
    def __init__(
        self,
        e,
        redundancy=2,
        espnow_header=bytearray([0xB2]),
    ):
        self.e = e
        self.redundancy = redundancy
        self.espnow_header = espnow_header
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
        if self.e is not None:
            data = self.serialize_update(update)
            self.e.send(data)
            for i in range(self.redundancy):
                self.e.send(data)
            self.increment_count()

    def serialize_update(self, update):
        buffer = bytearray(3)
        buffer[0] = update.key_number
        buffer[1] = update.pressed
        buffer[2] = self.sent_count
        return buffer

    def checksum(self, update):
        checksum = bytes([sum(update) & 0xFF])
        return checksum

