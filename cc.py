import mido
from parse import parse_elektron_manual
from sys import argv


def cc(outport, ch, addr, val):
    outport.send(mido.Message('control_change',
                              channel=ch,
                              control=addr,
                              value=val))
