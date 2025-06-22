import espnow

from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)


class RX_Aggregator(Module):
    def __init__(
        self,
        e,
        propagate_fault=None,
    ):
        self.e = e
        self.rx_buffer = []
        self.counter_tracker = {}
        self.propagate_fault = propagate_fault
        if propagate_fault is None:
            propagate_fault = []

    def during_bootup(self, keyboard):
        return

    def before_matrix_scan(self, keyboard):
        while True:
            packet = None
            try:
                packet = self.e.read()
            except ValueError:
                # workaround for issue #9816
                debug("ESP-NOW Error")
                for i in self.propagate_fault:
                    i.fault()
                peers = self.e.peers
                self.e.deinit()
                self.e = espnow.ESPNow()
                for peer in peers:
                    self.e.peers.append(peer)
                debug("recovered peers: ", self.e.peers)
                break
            if packet is None:
                break
            dest = packet.msg[0]
            count = packet.msg[1]
            if not dest in self.counter_tracker:
                self.counter_tracker.update({dest: None})
            if count == self.counter_tracker[dest]:
                break
            self.counter_tracker[dest] = count
            self.rx_buffer.append(packet.msg)

    def after_matrix_scan(self, keyboard):
        return

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

    def deinit(self, keyboard):
        self.e.deinit()
