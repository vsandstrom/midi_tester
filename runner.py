import json
import mido
from time import sleep
from random import randint
from sys import argv
from nrpn import nrpn as nrpn_msg, Data, Addr
from cc import cc as cc_msg
import toml

CC = 1

NRPN_MSB = 3
NRPN_LSB = 4

def nrpn_run(json, port, ch=0, n=15, dur=0.15):
    for row in midi:
        print(row['columns'][0] + row['columns'][1])
        for d in row['data']:
            msb = d[NRPN_MSB]
            lsb = d[NRPN_LSB]
            if msb is not None and lsb is not None:
                param = str(d[0])
                print('\t'+param+' \t\tNRPN: '+str(msb)+' :: '+str(lsb))
                for _ in range(0, n):
                    values = Data(randint(0, 127), randint(0, 127))
                    addr = Addr(int(msb), int(lsb))
                    nrpn_msg(port, ch, addr, values)
                    sleep(dur)

        print()


def cc_run(json, port, ch=0, n=15, dur=0.15):
    for row in midi:
        print(row['columns'][0] + row['columns'][1])
        for d in row['data']:
            cc = d[CC]
            if cc is not None:
                param = str(d[0])
                print('\t'+param+' \t\tNRPN: '+str(cc))
                for _ in range(0, n):
                    values = randint(0, 127)
                    addr = int(cc)
                    cc_msg(port, ch, addr, values)
                    sleep(dur)

        print()

if __name__ == "__main__":
    if argv[1] == "-h" or argv[1] == "--help":
        print("""
  Usage: takes two arguments\n\t
    port: midi receiver  ---------------------------------------------  [string]
    path: path to midi as JSON ( use backslash before space if macOS )  [string]
    ch:   midi channel to use  ---------------------------------------  [int]
    n:    test iterations  -------------------------------------------  [int]
    dur:  length of each iteration in seconds  -----------------------  [float]
        """)
        exit(0)

    with open("config.toml", "r") as t:
        t = toml.loads(t.read())['config']

    # path = "Digitone.json"
    mode = "nrpn"
    port = "IAC-drivrutin Buss 1"
    path = "Digitakt_II.json"
    ch = t['ch'] - 1
    n = t['iter']
    dur = t['dur']

    if argv[1]:
        mode = argv[1]
    if argv[2]:
        port = argv[2]
    if argv[3]:
        path = argv[3]

    outport = mido.open_output(port)
    with open(path, "r") as midi:
        midi = json.loads(str(midi.read()))

        # extract_nrpn(midi)
        if mode == 'nrpn':
            nrpn_run(midi, outport, ch, n, dur)
        elif mode == 'cc':
            cc_run(midi, outport, ch, n, dur)
        else:
            exit(-1)
