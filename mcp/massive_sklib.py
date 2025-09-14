from collections import defaultdict
from skidl import Pin, Part, Alias, SchLib, SKIDL, TEMPLATE

from skidl.pin import pin_types

SKIDL_lib_version = '0.0.1'

massive = SchLib(tool=SKIDL).add_parts(*[
        Part(**{ 'name':'C', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'C'}), 'ref_prefix':'C', 'fplist':[''], 'footprint':'Capacitor_SMD:C_0603_1608Metric', 'keywords':'cap capacitor', 'description':'Unpolarized capacitor', 'datasheet':'~', 'pins':[
            Pin(num='1',name='~',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='~',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'R', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'R'}), 'ref_prefix':'R', 'fplist':[''], 'footprint':'Resistor_SMD:R_0603_1608Metric', 'keywords':'R res resistor', 'description':'Resistor', 'datasheet':'~', 'pins':[
            Pin(num='1',name='~',func=pin_types.PASSIVE,unit=1),
            Pin(num='2',name='~',func=pin_types.PASSIVE,unit=1)], 'unit_defs':[] }),
        Part(**{ 'name':'ATmega8-16A', 'dest':TEMPLATE, 'tool':SKIDL, 'aliases':Alias({'ATmega8-16A'}), 'ref_prefix':'U', 'fplist':['Package_QFP:TQFP-32_7x7mm_P0.8mm', 'Package_QFP:TQFP-32_7x7mm_P0.8mm'], 'footprint':'Package_QFP:TQFP-32_7x7mm_P0.8mm', 'keywords':'AVR 8bit Microcontroller MegaAVR', 'description':'16MHz, 8kB Flash, 1kB SRAM, 512B EEPROM, TQFP-32', 'datasheet':'http://ww1.microchip.com/downloads/en/DeviceDoc/atmel-2486-8-bit-avr-microcontroller-atmega8_l_datasheet.pdf', 'pins':[
            Pin(num='29',name='PC6/~{RESET}',func=pin_types.BIDIR,unit=1),
            Pin(num='7',name='PB6/XTAL1',func=pin_types.BIDIR,unit=1),
            Pin(num='8',name='PB7/XTAL2',func=pin_types.BIDIR,unit=1),
            Pin(num='20',name='AREF',func=pin_types.PASSIVE,unit=1),
            Pin(num='19',name='ADC6',func=pin_types.INPUT,unit=1),
            Pin(num='22',name='ADC7',func=pin_types.INPUT,unit=1),
            Pin(num='4',name='VCC',func=pin_types.PWRIN,unit=1),
            Pin(num='6',name='VCC',func=pin_types.PASSIVE,unit=1),
            Pin(num='3',name='GND',func=pin_types.PWRIN,unit=1),
            Pin(num='5',name='GND',func=pin_types.PASSIVE,unit=1),
            Pin(num='18',name='AVCC',func=pin_types.PWRIN,unit=1),
            Pin(num='21',name='AGND',func=pin_types.PWRIN,unit=1),
            Pin(num='12',name='PB0',func=pin_types.BIDIR,unit=1),
            Pin(num='13',name='PB1',func=pin_types.BIDIR,unit=1),
            Pin(num='14',name='PB2',func=pin_types.BIDIR,unit=1),
            Pin(num='15',name='PB3',func=pin_types.BIDIR,unit=1),
            Pin(num='16',name='PB4',func=pin_types.BIDIR,unit=1),
            Pin(num='17',name='PB5',func=pin_types.BIDIR,unit=1),
            Pin(num='23',name='PC0',func=pin_types.BIDIR,unit=1),
            Pin(num='24',name='PC1',func=pin_types.BIDIR,unit=1),
            Pin(num='25',name='PC2',func=pin_types.BIDIR,unit=1),
            Pin(num='26',name='PC3',func=pin_types.BIDIR,unit=1),
            Pin(num='27',name='PC4',func=pin_types.BIDIR,unit=1),
            Pin(num='28',name='PC5',func=pin_types.BIDIR,unit=1),
            Pin(num='30',name='PD0',func=pin_types.BIDIR,unit=1),
            Pin(num='31',name='PD1',func=pin_types.BIDIR,unit=1),
            Pin(num='32',name='PD2',func=pin_types.BIDIR,unit=1),
            Pin(num='1',name='PD3',func=pin_types.BIDIR,unit=1),
            Pin(num='2',name='PD4',func=pin_types.BIDIR,unit=1),
            Pin(num='9',name='PD5',func=pin_types.BIDIR,unit=1),
            Pin(num='10',name='PD6',func=pin_types.BIDIR,unit=1),
            Pin(num='11',name='PD7',func=pin_types.BIDIR,unit=1)], 'unit_defs':[] })])