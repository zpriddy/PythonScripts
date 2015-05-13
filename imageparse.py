#! /usr/bin/python
#################################################
#			Image Parser 						#
#################################################
# Zachary Priddy - 2015 						#
# me@zpriddy.com 								#
#												#
# REQUIRES hexparse.py 							#
#################################################
#################################################


import sys, argparse, binascii, hexparse


def main():
	parser = argparse.ArgumentParser(prog="Image PArse")
	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument("-s", "--string", help="Enter String in single quotes of the pcap data") 
	group.add_argument("-f", "--file", help="Enter File containing the hex dump of the dns query request") 
	parser.add_argument("-d", "--debug", help="Set flag for debug info",action='store_true') 
	args = parser.parse_args()

	debug = args.debug

	lines=""
	hexstring=""

	if args.string:
		#print args.string
		lines= args.string.split("\n")

	elif args.file:
		lines = open(args.file,'r')
		
	try:
		for line in lines:
			hexstring = hexstring + hexparse.parse_hex_data(line)
	except:
		print "IS NOT HEX"
		exit();

	hexstring = hexstring.upper().replace("X","x")

	if(debug):
		print hexstring

	start_index=hexstring.find("\\xFF\\xD8\\xFF")
	end_index=hexstring.rfind("\\xFF\\xD9")
	potential_images=hexstring.count("\\xFF\\xD8\\xFF")
	if(debug):
		print "Start Index: \t", start_index
		print "End Index: \t", end_index
	print "Potential Images (JPEG):\t", potential_images 
	#print "Potential Images (footer): ", hexstring.count("\\xFF\\xD9")

	file_count=1
	for image in range(1,potential_images+1):
		test_image=hexstring[start_index:end_index+8].replace("\\x","")
		hexdata = binascii.unhexlify(b'%s' % test_image)
		output_name = "output" + str(file_count) + ".jpg"
		output_file = open(output_name,'wb')
		output_file.write(hexdata)
		output_file.close()
		file_count+=1
		start_index=hexstring.find("\\xFF\\xD8\\xFF",start_index+12)
		if(debug):
			print "Start Index: \t", start_index


	#PNG FILE SEARCH

	start_index=hexstring.find("\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A")
	potential_images=hexstring.count("\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A")
	if(debug):
		print "Start Index: \t", start_index
	print "Potential Images (PNG): \t", potential_images

	file_count=1
	for image in range(1,potential_images+1):
		test_image=hexstring[start_index:].replace("\\x","")
		hexdata = binascii.unhexlify(b'%s' % test_image)
		output_name = "output" + str(file_count) + ".png"
		output_file = open(output_name,'wb')
		output_file.write(hexdata)
		output_file.close()
		file_count+=1
		start_index=hexstring.find("\\x89\\x50\\x4E\\x47\\x0D\\x0A\\x1A\\x0A",start_index+32)
		if(debug):
			print "Start Index: \t", start_index

	#GIF FILES

	start_index=hexstring.find("\\x47\\x49\\x46\\x38\\x37\\x61")
	potential_images=hexstring.count("\\x47\\x49\\x46\\x38\\x37\\x61")
	if(debug):
		print "Start Index: \t", start_index
	print "Potential Images (GIF): \t", potential_images

	file_count=1
	for image in range(1,potential_images+1):
		test_image=hexstring[start_index:].replace("\\x","")
		hexdata = binascii.unhexlify(b'%s' % test_image)
		output_name = "output" + str(file_count) + ".gif"
		output_file = open(output_name,'wb')
		output_file.write(hexdata)
		output_file.close()
		file_count+=1
		start_index=hexstring.find("\\x47\\x49\\x46\\x38\\x37\\x61",start_index+24)
		if(debug):
			print "Start Index: \t", start_index

	start_index=hexstring.find("\\x47\\x49\\x46\\x38\\x39\\x61")
	potential_images=hexstring.count("\\x47\\x49\\x46\\x38\\x39\\x61")
	if(debug):
		print "Start Index: \t", start_index
	print "Potential Images (GIF 2):\t", potential_images

	file_count=1
	for image in range(1,potential_images+1):
		test_image=hexstring[start_index:].replace("\\x","")
		hexdata = binascii.unhexlify(b'%s' % test_image)
		output_name = "output" + str(file_count) + "_2.gif"
		output_file = open(output_name,'wb')
		output_file.write(hexdata)
		output_file.close()
		file_count+=1
		start_index=hexstring.find("\\x47\\x49\\x46\\x38\\x39\\x61",start_index+24)
		if(debug):
			print "Start Index: \t", start_index


if __name__ == '__main__':
   main()