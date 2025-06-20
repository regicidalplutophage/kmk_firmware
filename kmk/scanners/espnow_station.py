import espnow

from keypad import Event as KeyEvent

from kmk.scanners import Scanner
from kmk.utils import Debug

debug = Debug(__name__)


class ESPNOW_Station(Scanner):
    def __init__(
        self,
        e,
        key_count = 0,
        offset = 0,
        header=bytearray([0xB2]),
    ):
        self.e = e
        self.header = header
        self.kevent_buffer = []
        self._key_count = key_count
        self.offset = offset
        self.last_success = None

    @property
    def key_count(self):
        return self._key_count

    def scan_for_changes(self):
        if self.e is not None:
            while True:
                packet = None
                try:
                    packet = self.e.read()
                except ValueError as error:
                    # workaround for issue #9816
                    debug("ESP-NOW Error")
                    self.emergency_release()
                    peers = self.e.peers
                    self.e.deinit()
                    self.e = espnow.ESPNow()
                    for peer in peers:
                        self.e.peers.append(peer)
                    debug("recovered peers: ", self.e.peers)
                    break
                if packet is None:
                    break
                if packet.msg[2] == self.last_success:
                    break
                self.last_success = packet.msg[2]
                self.kevent_buffer.append(self.deserialize_update(packet.msg))

            if self.kevent_buffer:
                return self.kevent_buffer.pop(0)

    def checksum(self, update):
        checksum = bytes([sum(update) & 0xFF])
        return checksum

    def emergency_release(self):
        for i in range(self.key_count):
            kevent = KeyEvent(key_number=i + self.offset, pressed=0)
            self.kevent_buffer.append(kevent)


    def deserialize_update(self, update):
        kevent = KeyEvent(key_number=update[0] + self.offset, pressed=update[1])
        return kevent
