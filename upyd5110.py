# -*- coding: utf-8 -*- 
# library of display Nokia 5110 for micropython
# datasheet pcd8544 here: http://ziblog.ru/wp-content/uploads/2013/03/Nokia5110.pdf
#
# memo I/Os
# display     pyboard   state
# DIN    ->   Y7
# CLK    ->   Y6
# RST    ->   Y4        active 0
# CE     ->   Y5        must be 0 or gnd
# DC     ->   Y3        commands 0, data 1
# VCC    ->   3.3V
# LIGHT  ->   Y2        active 0
# GND    ->   GND

import pyb

class Display:
  def __init__(self, spi, rst, ce, dc, light):
    
    # init the SPI bus and pins
    spi.init(spi.MASTER, baudrate=328125, bits=8, polarity=0, phase=1, firstbit=spi.MSB)
    rst.init(rst.OUT_PP, rst.PULL_NONE)
    ce.init(ce.OUT_PP, ce.PULL_NONE)
    dc.init(dc.OUT_PP, dc.PULL_NONE)
    light.init(light.OUT_PP, light.PULL_NONE)
    
    # store the pins
    self.spi = spi
    self.rst = rst
    self.ce = ce
    self.dc = dc
    self.light = light
    
    # reset everything
    self.ce.high()
    self.light.high()
    self.rst.low() # A RST pulse must be applied
    pyb.udelay(10)
    self.rst.high()
    
    # example from datashit p.22
    self.ce.low()
    self.dc.low()
    self.spi.send(b'\x90')
    self.spi.send(b'\x20')
    self.spi.send(b'\x0C')
    self.dc.high()
    self.spi.send(b'\x1F')
    self.spi.send(b'\x05')
    self.spi.send(b'\x07')
    self.spi.send(b'\x00')
    self.spi.send(b'\x1F')
    self.spi.send(b'\x04')
    self.spi.send(b'\x1F')
    self.dc.low()
    self.spi.send(b'\x0D')
    self.spi.send(b'\x80')
    
    
  def light_on(self):
    self.light.low()
    
  def light_off(self):
    self.light.high()
    
  def command(self, buf):
    self.ce.low()
    self.dc.low()
    self.spi.send(buf)
    
  def write(self, buf, X, Y):
    assert X <= 83
    assert Y <= 5
    xbyte = X + 128
    xbyte = xbyte.to_bytes(1)
    ybyte = Y + 64
    ybyte = ybyte.to_bytes(1)
    self.ce.low()
    self.dc.low() # command mode
    self.spi.send(xbyte)
    self.spi.send(ybyte)
    self.dc.high() # data mode
    self.spi.send(buf)
    
#from main.py
#SPI    = pyb.SPI(1)
#RST    = pyb.Pin('Y4')
#CE     = pyb.Pin('Y5')
#DC     = pyb.Pin('Y3')
#LIGHT  = pyb.Pin('Y2')
#dsp = Display(SPI, RST, CE, DC, LIGHT)
