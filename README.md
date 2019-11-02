Pi Term for RC6502
===

This application is intended to be used with the RC6502 Apple 1 replica from https://github.com/tebl/RC6502-Apple-1-Replica

Connect the RPi in place of the Arduino nano as shown in the table below and then run the rpi_rc6502.py application with python 3. The Raspberry Pi replaces Arduino + PC.

## Connections

RC6502 | Nano | RPi | In/Out (from Pi)
-------|------|-----|-------:
TX | 1 - D1 - TX | Not needed | Out
RX | 2 - D0 - RX | Not needed | In
KBD_READY | 5 - D2 - INT0 | 12 - GPIO18 | In
KBD_STROBE | 7 - D4 - T0 | 18 - GPIO24 | Out
OUT_DA | 6 - D3 - INT2 | 16 - GPIO23 | In
OUT_RDA | 8 - D5 - T1 | 22 - GPIO25 | Out
SS | 13 - D10 - SS | 24 - GPIO08 - SPI_CE0_N | Out
SCK | 16 - D13 -SCK | 23 - GPIO11 - SPIO-SCLK | Out
MOSI | 14 - D11 - MOSI | 19 - GPIO10 - SPIO-MOSI | Out
MISO | 15 - D12 - MISO | 21 - GPIO9 - SPIO-MISO  | In
P_RESET | 28 - RESET | 8 - GPIO14 - UART0_TXD | Out 
5V | 27 - 5V | 2 - 5V | Out
GND | 29 - GND | 9 - GND | Out

