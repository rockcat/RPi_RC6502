
import RPi.GPIO as GPIO
from RPiMCP23S17.MCP23S17 import MCP23S17
import sys
import curses
from curses import wrapper
from curses import ascii
from time import sleep
import signal

CTRL_X = 24

# BOARD mode - PIN numbers
KBD_READY = 12
KBD_STROBE = 18
OUT_DA = 16
OUT_RDA = 22
P_RESET = 8

SPI_BUS = 0
SPI_CS = 0

mcp = MCP23S17(bus = SPI_BUS, pin_cs = SPI_CS,
               pin_reset = P_RESET, device_id = 0)

def mcp_setup():
    mcp.open()
    mcp._spi.max_speed_hz = 100000
    for i in range(0, 8):
        mcp.setDirection(i, mcp.DIR_INPUT)
        mcp.setDirection(i+8, mcp.DIR_OUTPUT)
    for i in range(0, 16):
        mcp.setPullupMode(i, MCP23S17.PULLUP_DISABLED)
    mcp.setPullupMode(7, MCP23S17.PULLUP_ENABLED)

def getPortA():
    inp = mcp.readGPIO()
    inp = inp & 0xFF
    return inp

def setPortB(val):
    mcp.writeGPIO((val & 0xFF) << 8)

def gpio_setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(KBD_READY, GPIO.IN)
    GPIO.setup(KBD_STROBE, GPIO.OUT)
    GPIO.setup(OUT_DA, GPIO.IN)
    GPIO.setup(OUT_RDA, GPIO.OUT)
    GPIO.setup(P_RESET, GPIO.OUT)

    GPIO.output(KBD_STROBE, GPIO.LOW)
    GPIO.output(OUT_RDA, GPIO.LOW)

# send character to 6502
def send(ch):
    if ch == 10:                       # convert LF to CR for Apple 1
        ch = 13
    if ch == curses.KEY_BACKSPACE:     # convert BKSPC to 95 for Apple 1
        ch = 0x5F
    if ch < 96:
        setPortB(ch | 0x80)
        GPIO.output(KBD_STROBE, GPIO.HIGH)
        GPIO.output(KBD_STROBE, GPIO.LOW)

# get character from 6502 or -1 if none
def recieve():
    ch = -1
    if GPIO.input(OUT_DA):
        ch = getPortA() & 0x7F
        GPIO.output(OUT_RDA, GPIO.HIGH)
        GPIO.output(OUT_RDA, GPIO.LOW)
        if ch == 13:
            ch = 10
    return ch

def initTerminal():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.clear()
    stdscr.nodelay(1)
    stdscr.scrollok(1)
    stdscr.addstr('RPi RC6502 Terminal by rockcat\nCtrl-X to quit\n\n')
    stdscr.refresh()
    return stdscr

def quit(stdscr):
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()
    sys.exit(0)

def delCh(stdscr):
    y, x = stdscr.getyx()
    if x > 0:
        x = x -1
    stdscr.move(y, x)
    stdscr.delch(y, x)

def process(stdscr):
   
    while True:
        inp = stdscr.getch()
        if inp == CTRL_X:
            quit(stdscr)
        if inp != curses.ERR:
            if ascii.islower(inp):
                inp = inp - 32              # to upper case
            send(inp)
        outp = recieve()
        if outp == 0x5F:            # APPLE1 del character
            delCh(stdscr)
        elif outp >= 0:
            stdscr.addch(outp)
            stdscr.refresh()

def ctrlc_handler(sig, frame):
    send(3)
    return

def main():
    signal.signal(signal.SIGINT, ctrlc_handler)
    gpio_setup()
    mcp_setup()
    stdscr = initTerminal()
    process(stdscr)

main()
