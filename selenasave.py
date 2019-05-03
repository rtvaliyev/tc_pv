import telnetlib
import time
import csv
import os


def savellet():
	lines_seen = set()
	outfile = open("noduplicate.txt", "w")
	for line in open("saved.txt", "r"):
		if line not in lines_seen:
			outfile.write(line)
			lines_seen.add(line)
	outfile.close()
	with open('noduplicate.txt') as save_file:
		save_reader = csv.reader(save_file, delimiter=',')
		for row in save_reader:
			if "64portluqhuawei"==row[2]:
				user1 = "dslam login username"
				password1 = "dslam login pass"
				tn = telnetlib.Telnet(row[1])
				tn.read_until(b">>User name:")
				tn.write(user1.encode('ascii') + b"\n")
				if password1:
					tn.read_until(b">>User password:")
					tn.write(password1.encode('ascii') + b"\n")
				tn.write(b"enable\n")
				time.sleep(1)
				tn.write(b"save\n\n")
				tn.read_until(b"{ <cr>|configuration<K>|data<K> }:")
				time.sleep(1)
				tn.write(b"quit\n")
				tn.write(b"y\n")
				gg = tn.read_all().decode('ascii')
				yesdir2 = gg.splitlines()[2]
				if yesdir2 == "  Command:":
					dslam_adi2 = gg.splitlines()[12]
					success2 = gg.splitlines()[3]
					with open('resultselena.txt', 'a') as result:
						result.write(dslam_adi2[:-1]+' '+success2[:-1]+ 'd successfully. || ' '\n')
			if "48portluqhuawei"==row[2]:
				user1 = "dslam login username"
				password1 = "dslam login pass"
				tn = telnetlib.Telnet(row[1])
				tn.read_until(b"Username:")
				tn.write(user1.encode('ascii') + b"\n")
				if password1:
					tn.read_until(b"Password:")
					tn.write(password1.encode('ascii') + b"\n")
				tn.write(b"enable\n\n")
				time.sleep(1)
				tn.write(b"write\n\n")
				tn.write(b"y")
				tn.write(b"exit\n")
				gg = tn.read_all().decode('ascii')
				yesdir2 = gg.splitlines()[14]
				yesdir2nzs = gg.splitlines()[14]
				if yesdir2 == "Write configuration to flash memory successfully.":
					dslam_adi2 = gg.splitlines()[4]
					success2 = gg.splitlines()[14]
					with open('resultselena.txt', 'a') as result:
						result.write(dslam_adi2[:-1]+' saved '+success2[35:]+' || \n')
				if yesdir2nzs == "Write running configuration to flash memory successfully.":
					dslam_adi2 = gg.splitlines()[16]
					success2 = gg.splitlines()[14]
					with open('resultselena.txt', 'a') as result:
						result.write(dslam_adi2[:-1]+' saved '+success2[43:]+' || \n')
	with open('resultselena.txt') as result:
		return result


def delellet():
	# with open('saved.txt', 'w') as emptylist:
	# 	emptylist.write('')
	# with open('resultselena.txt', 'w') as result:
	# 	result.write('')
	os.remove("resultselena.txt")
	os.remove("saved.txt")
	os.remove("noduplicate.txt")
	
