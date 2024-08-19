import mido
from parse import parse_elektron_manual
from sys import argv

MSB = 99
LSB = 98
DT1 = 6
DT2 = 38


class Addr:
    """
    Contains the address component of an NRPN message
    It is up to the user to use valid numbers [0 - 127]
    """

    def __init__(self, msb, lsb):
        self.msb = msb
        self.lsb = lsb


class Data:
    """
    Contains the data component of an NRPN message
    It is up to the user to use valid numbers [0 - 127]
    """

    def __init__(self, coarse, fine):
        self.coarse = coarse
        self.fine = fine


def nrpn(outport, ch: int, addr: Addr, val: Data):
    outport.send(mido.Message("control_change",
            channel=ch, control=MSB, value=addr.msb
        )
    )

    outport.send(mido.Message("control_change",
            channel=ch, control=LSB, value=addr.lsb
        )
    )
    outport.send(mido.Message("control_change",
            channel=ch, control=DT1, value=val.coarse
        )
    )

    outport.send(mido.Message("control_change",
            channel=ch, control=DT2, value=val.fine
        )
    )


if __name__ == "__main__":
    port = "IAC-drivrutin Buss 1"
    if argv[1] is not None:
        port = argv[1]

    outport = mido.open_output(port)
    nrpn(outport, 0, Addr(1, 0), Data(20, 69))
