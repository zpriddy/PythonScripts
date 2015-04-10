#! /usr/bin/python
#################################################
#			Python HEX Tools					#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
#################################################
#################################################


import array, binascii, string, StringIO, sys, argparse


def main():
	parser = argparse.ArgumentParser(prog="Hex Parse")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-s", "--string", help="Enter String in single quotes of the pcap data") 
	group.add_argument("-f", "--file", help="Enter File containing the hex dump of the dns query request")
	parser.add_argument("-b", "--binary", help="Use this option if the input file is a binary file",action="store_true")
	parser.add_argument("-x", "--hex", help="Use this option if the input file is a hexdump",action="store_true")
	args = parser.parse_args()

	data = ""

	if args.string:
		#print args.string
		lines= args.string.split("\n")

	elif args.file:
		lines = open(args.file,'r')
		if(args.binary):
			raw = binascii.hexlify(lines.read()).split("\n")
			lines = raw


	try:
		for line in lines:
			data = data + parse_hex_data(line)

		print data
	except:
		print "IS NOT HEX"



def is_hex(string):
   try:
       int(string, 16)
       return True
   except ValueError:
       return False

def parse_hex_data(input_string, max_width=16):
	if(max_width%2 != 0):
		return 'ERROR: ODD MAX WIDTH'

	hex_output = ""
	#Drop leading spaces
	if(input_string[0] == " "):
		while(input_string[0] == " "):
			input_string = input_string[1:]

	#Replace double spaces
	input_string = input_string.replace("  "," ")

	#SPLIT INPUT BY STRING
	test_string = input_string.split(" ")

	

	## NO SPACES IN INPUT
	if(len(test_string) == 1):
		#See if its in the format %00 with no spaces
		if(input_string.count("%") > len(test_string)/3):
			input_string = input_string.replace(" ","").upper().replace("%","\\x")
			hex_output = input_string
		#See if its in the format \x00 with no spaces
		elif(input_string.count("\\x") > len(test_string)/3):
			input_string = input_string.replace(" ","").upper().replace("X","x")
			hex_output = input_string
		#else single hex string
		else:
			if(len(input_string) % 2 == 0):
				for i in range(0,len(input_string)/2):
					hex_output = hex_output + "\\x" + input_string[i*2:i*2+2]

	##SPACES IN INPUT
	else:
		#See if its in the format \x00
		if(input_string.count("\\x") > len(test_string)-1):
			input_string = input_string.replace(" ","").upper().replace("X","x")
			hex_output = input_string
		#See if its in the format %00
		elif(input_string.count("%") > len(test_string)-1):
			input_string = input_string.replace(" ","").upper().replace("%","\\x")
			hex_output = input_string
		##IF first two elements the same length only copy elements that are the same length NO ADDRESS
		elif(len(test_string[0]) == len(test_string[1])):
			temp_string = ""
			length_ok = len(test_string[0])
			for i in range(0,len(test_string)):
				if(len(test_string[i]) == length_ok):
					temp_string = temp_string + test_string[i]
			if(len(temp_string) < max_width):
				max_width = len(temp_string)
			for i in range(0,max_width/2):
				hex_output = hex_output + "\\x" + temp_string[i*2:i*2+2]

		##IF SECOND AND THRID ELEMENTS ARE THE SAME LENGTH - SAME LOGIC HAS ADDRESS
		elif(len(test_string[1]) == len(test_string[2])):
			temp_string = ""
			length_ok = len(test_string[1])
			for i in range(0,len(test_string)):
				if(len(test_string[i]) == length_ok):
					if(is_hex(test_string[i]) and i <= max_width):
						temp_string = temp_string + test_string[i]
			if(len(temp_string) < max_width):
				max_width = len(temp_string)
			for i in range(0,max_width/2):
				hex_output = hex_output + "\\x" + temp_string[i*2:i*2+2]

	hex_output = hex_output.upper().replace("X","x")

	if(is_hex(hex_output.replace("\\x",""))):

		return hex_output

	else:
		raise NameError('IsNotHex')



if __name__ == '__main__':
   main()
