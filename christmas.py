import time
import telnetlib

# IP for the Prismatik API
host = '127.0.0.1'

# Port for the Prismatik API
port = 3636

# The order and grouping of LEDs:
# The colors will cycle through the LEDs in this order. Put multiple LED numbers in the same
# list and they will both be the same color
leds = [
    [1, 10], # 1 and 10 will always be the same color
    [2],
    [3],
    [4],
    [5],
    [6],
    [7],
    [8],
    [9],
]

# Colors to cycle through
colors = [
    '255,0,0',
    '0,255,0',
    #'0,0,255'
]

# Telnet to the Prismatik API
tn = telnetlib.Telnet(host, port)

# Wait until it's ready
tn.read_until("Lightpack API".encode('ascii'))

# Send the 'lock' command so we can change LEDs
tn.write("lock\r\n".encode('ascii'))

tn.read_until("lock:success".encode('ascii'))


def cycle(stop_after=None):

    i = 0

    while True:
        color = i % len(colors)
        # Build a string of which color every LED should be
        command = "setcolor:"

        for led_set in leds:

            for led in led_set:
                rgb = colors[color]
                command += str(led) + "-" + rgb + ";"

            color += 1
            if color >= len(colors):
                color = 0

        # Send the command
        tn.write((command + "\r\n").encode('ascii'))

        tn.read_until("ok".encode('ascii'))

        time.sleep(1)
        i += 1
        if stop_after and i >= stop_after:
            return


cycle()
