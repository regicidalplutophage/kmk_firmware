from keypad import Event as KeyEvent

from kmk.scanners import Scanner
from kmk.utils import Debug

debug = Debug(__name__)


class RX_Scanner(Scanner):
    def __init__(
        self,
        rx_buffer,
        address=0,
        key_count=0,
        offset=0,
    ):
        self.rx_buffer = rx_buffer
        self.address = address
        self.kevent_buffer = []
        self._key_count = key_count
        self.offset = offset

    @property
    def key_count(self):
        return self._key_count

    def scan_for_changes(self):
        for i, packet in enumerate(self.rx_buffer):
            if packet[0] != self.address:
                continue
            kevent = self.deserialize(self.rx_buffer.pop(i))
            self.kevent_buffer.append(kevent)

        if self.kevent_buffer:
            return self.kevent_buffer.pop(0)

    # def checksum(self, update):
    #     checksum = bytes([sum(update) & 0xFF])
    #     return checksum

    def fault(self):
        for i in range(self.key_count):
            kevent = KeyEvent(key_number=i + self.offset, pressed=0)
            self.kevent_buffer.append(kevent)

    def deserialize(self, update):
        kevent = KeyEvent(key_number=update[2] + self.offset, pressed=update[3])
        return kevent
