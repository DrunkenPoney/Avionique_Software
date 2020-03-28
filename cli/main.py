"""Command line test program to send commands to the comm-module."""


# imports
import sys
import serial
import struct
import pycrc.algorithms as crcalgo


# global configuration variables
BAUD_RFD = 115200
CMD_PKT_FMT = '>HHBB'
START_SHORT = 0xface
CRC = crcalgo.Crc(width=16, poly=0x1021,
				reflect_in=False, reflect_out=False,
				xor_in=0xffff, xor_out=0x0000)


def print_help():
	print('Syntax: > [function] [args]')
	print('Supported functions are:')
	print('set - set an actuator to a high state')
	print('\targ is the number of the actuator')
	print('reset - reset an actuator to a low state')
	print('\targ is the number of the actuator')
	print('exit - quit the command line tool')


def compute_crc(data):
	return CRC.bit_by_bit(data)


def set_actuator(ser, i, a):
	data = struct.pack(CMD_PKT_FMT, START_SHORT, i, 1, a)
	data = struct.pack(CMD_PKT_FMT + 'H', data, compute_crc(data))
	print('writing:', data)
	size = ser.write(data)
	print('wrote:', size)


def reset_actuator(ser, i, a):
	data = struct.pack(CMD_PKT_FMT, START_SHORT, i, 2, a)
	data = struct.pack(CMD_PKT_FMT + 'H', data, compute_crc(data))
	print('writing:', data)
	size = ser.write(data)
	print('wrote:', size)


def cli(port):
	i = 0
	with serial.Serial(port, BAUD_RFD, timeout=1) as ser:
		while True:
			print(ser.timeout)
			# get input
			s = input('> ')
			# treat simple functions first
			if s == '-h' or s == '--help':
				print_help()
			elif s == 'exit':
				break
			# get function and arguments
			try:
				f, a = s.split(' ')
				a = int(a) 
			except ValueError as e:
				print('Invalid command, error occured:', e)
				continue
			# treat function calls
			if f == 'set':
				set_actuator(ser, i, a)
			elif f == 'reset':
				reset_actuator(ser, i, a)
			else:
				print('Invalid command, type -h or --help for help')
			i += 1


if __name__ == '__main__':
	port = sys.argv[1]
	cli(port)

	sys.exit(0)
