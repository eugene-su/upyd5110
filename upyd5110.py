# -*- coding: utf-8 -*- 
# Micropython board 1.0 library for Nokia 5110 display
# author: Евгений
# license: Apache 2.0
# original: https://github.com/inaugurator/upyd5110
# datasheet: https://www.sparkfun.com/datasheets/LCD/Monochrome/Nokia5110.pdf
# Micropython project: http://micropython.org/
# One data byte is vertical column with LSB on the top.
# SPI mode bits=8, polarity=0, phase=1
# 
# Pins definition
# display     pyboard           state
#
# VCC    ->   3V3 or any Pin    3.3V
# DIN    ->   MISO
# CLK    ->   SCK               0 - 4 MHz
# RST    ->   any Pin           active 0, at start it may be 0
# CE     ->   any Pin           for start transmission 0
# DC     ->   any Pin           commands 0, data 1
# LIGHT  ->   any Pin           active 0
# GND    ->   GND
#
# First side
# SPI    = pyb.SPI(1)
# RST    = pyb.Pin('Y4')
# CE     = pyb.Pin('Y5')
# DC     = pyb.Pin('Y3')
# LIGHT  = pyb.Pin('Y2')
# PWR    = pyb.Pin('Y1')
#
# Second side
# SPI    = pyb.SPI(2)
# RST    = pyb.Pin('X4')
# CE     = pyb.Pin('X5')
# DC     = pyb.Pin('X3')
# LIGHT  = pyb.Pin('X2')
# PWR    = pyb.Pin('X1')

import pyb # module for operation of the periphery

# main class
class Display:
  def __init__(self, spi, rst, ce, dc, light, pwr):
    
    # init the SPI bus and pins
    spi.init(spi.MASTER, baudrate=328125, bits=8, polarity=0, phase=1, firstbit=spi.LSB)
    rst.init(rst.OUT_PP, rst.PULL_NONE)
    ce.init(ce.OUT_PP, ce.PULL_NONE)
    dc.init(dc.OUT_PP, dc.PULL_NONE)
    light.init(light.OUT_PP, light.PULL_NONE)
    pwr.init(pwr.OUT_PP, pwr.PULL_NONE)
    
    # store the pins
    self.spi   = spi
    self.rst   = rst
    self.ce    = ce
    self.dc    = dc
    self.light = light
    self.pwr   = pwr
    
    # light off
    self.lightOff()
    
    # turn on
    self.turnOn() # power on
    self.command(b'\x21') # extended command mode
    self.command(b'\xC8') # for 3.3V power supply
    self.command(b'\x06') # set temperature correction
    self.command(b'\x13') # system bias
    self.command(b'\x20') # basic command mode
    self.command(b'\x0C') # b/w mode, horizontal addressing
    self.clear()
    
  # power on
  def turnOn(self):
    self.pwr.high()
    self.reset()

  # this needs for proper initialization
  def reset(self):
    self.rst.low() # rst active 0
    pyb.udelay(100) # reset impulse have to be > 100 ns and < 100 ms
    self.rst.high() # deactivate rst

  # display have to be blank before power off
  def turnOff(self):
    self.clear()
    self.command(b'\x20') # basic command mode
    self.command(b'\x08') # clear the display
    pyb.delay(10)
    self.pwr.low() # turn off power supply pin
    
  
  def clear(self):
    self.command(b'\x20') # basic command mode
    self.command(b'\x80') # set X address = 0
    self.command(b'\x40') # set Y address = 0
    self.write(b'\x00'*504) # fill RAM with '0's
  
  
  def command(self, buf):
    assert type(buf) == type(bytes()) # check that buf is bytes
    assert len(buf) == 1 # check that buf is one byte
    self.dc.low() # command mode
    self.write(buf) # write command
    self.dc.high() # return to data mode
  
  
  def write(self, buf):
    assert type(buf) == type(bytes()) # check that buf is bytes
    self.ce.low() # start transmission
    self.spi.send(buf) # 
    self.ce.high() # end transmission


  def setXY(self, X, Y):
    assert X <= 83 # X may be 0-83
    assert Y <= 5 # Y may be 0-5
    xbyte = X + 128 # X address is 0b1xxxxxxx
    xbyte = xbyte.to_bytes(1) # convert dex to bin
    ybyte = Y + 64 # Y address is 0b01000xxx
    ybyte = ybyte.to_bytes(1) # convert dex to bin
    self.command(b'\x20') # basic command mode
    self.command(xbyte) # set X address
    self.command(ybyte) # set Y address
    
  
  def lightOn(self):
    self.light.low() # active 0


  def lightOff(self):
    self.light.high() # inactive 1
