from bs4 import BeautifulSoup
import requests
import telnetlib
import time
import csv


def gellet(usernam,passwor,nomre):
	s = requests.Session()
	# Asagida POST melumatlari qeyd olunmalidir,misalcun:
	data = {
			'txtLogin':usernam,
			'txtPwd':passwor,
			'btnSubmit':'Submit'
			}
	login_request = s.post('billing-e login olmaq ucun link', data=data)
	# Asagida POST melumatlari qeyd olunmalidir,misalcun:
	data1 = {
			'srchLogin':nomre,
			}
	req1 = s.post('nomresini sorgulamaq ucun link', data=data1)
	soup = BeautifulSoup(req1.text,'html.parser')
	content = soup.find_all('a')
	for links in content:
		link = links['href']
		if "view_user_info&id" in link:
			userlink = 'nomrenin linki'+link
			req2 = s.get(userlink)
			soup1 = BeautifulSoup(req2.text,'html.parser')
			ipdslam = soup1.find('td', text='DSLAM').find_next('td').text.strip()
			ipplata = soup1.find('td', text='Plate').find_next('td').text.strip()
			ipport = soup1.find('td', text='Port').find_next('td').text.strip()
			sipport = soup1.find('td', text='Phone').find_next('td').text.strip()
			ipTariff = soup1.find('td', text='Tariff').find_next('td').text.strip()

			with open('hostlar.txt') as txt_file:
				txt_reader = csv.reader(txt_file, delimiter=',')
				for row in txt_reader:
					if ipdslam==row[0] and int(ipplata)>0:
						if "64portluqhuawei"==row[2]:
							with open('speeds64.txt') as speeds64_file:
								speeds64_reader = csv.reader(speeds64_file, delimiter=',')
								for sp in speeds64_reader:
									if ipTariff==sp[0]:
										with open('saved.txt', 'a') as output:
											output.write(row[0]+','+row[1]+','+row[2]+'\n')
										profayl=sp[1]
										user = "dslam login username"
										password = "dslam login pass"
										tn = telnetlib.Telnet(row[1])
										tn.read_until(b">>User name:")
										tn.write(user.encode('ascii') + b"\n")
										if password:
											tn.read_until(b">>User password:")
											tn.write(password.encode('ascii') + b"\n")
										tn.write(b"enable\n")
										tn.write(b"config\n")
										tn.write(b"interface adsl 0/")
										tn.write(ipplata.encode('ascii') + b"\n")
										time.sleep(1)
										tn.write(b"deactivate ")
										time.sleep(1)
										tn.write(ipport.encode('ascii') + b"\n")
										time.sleep(1)
										tn.write(b"activate ")
										tn.write(ipport.encode('ascii') + b" profile-index ")
										time.sleep(1)
										tn.write(profayl.encode('ascii') + b"\n")
										time.sleep(1)
										tn.read_until(b"#")
										time.sleep(1)
										tn.write(b"quit\n")
										tn.write(b"quit\n")
										tn.write(b"quit\n")
										tn.write(b"y\n")
										hh = tn.read_all().decode('ascii')
										yesdir = hh.splitlines()[0]
										if yesdir == "config":
											dslam_adi1 = hh.splitlines()[22]
											success1 = hh.splitlines()[12]
											print (success1)
											a=[dslam_adi1,ipplata,ipport,ipTariff,success1]
											return a
						if "48portluqhuawei"==row[2]:
							with open('speeds48.txt') as speeds48_file:
								speeds48_reader = csv.reader(speeds48_file, delimiter=',')
								for sp in speeds48_reader:
									if ipTariff==sp[0]:
										with open('saved.txt', 'a') as output:
											output.write(row[0]+','+row[1]+','+row[2]+'\n')
										profayl=sp[1]
										print(" ")
										user = "dslam login username"
										password = "dslam login pass"
										tn = telnetlib.Telnet(row[1])
										tn.read_until(b"Username:")
										tn.write(user.encode('ascii') + b"\n")
										if password:
											tn.read_until(b"Password:")
											tn.write(password.encode('ascii') + b"\n")
										tn.write(b"enable\n\n")
										tn.read_until(b"#")
										tn.write(b"configure terminal\n")
										tn.write(b"adsl deactivate adsl ")
										tn.write(ipplata.encode('ascii'))
										tn.write(b"/0/")
										tn.write(ipport.encode('ascii') + b"\n\n")
										time.sleep(1)
										tn.write(b"adsl activate adsl ")
										tn.write(ipplata.encode('ascii'))
										tn.write(b"/0/")
										tn.write(ipport.encode('ascii')+ b" ")
										tn.write(profayl.encode('ascii') + b"\n")
										time.sleep(1)
										tn.write(b"exit\n")
										time.sleep(1)
										tn.write(b"show adsl line state adsl ")
										tn.write(ipplata.encode('ascii'))
										tn.write(b"/0/")
										tn.write(ipport.encode('ascii') + b"\n")
										time.sleep(1)
										tn.write(b"\n")
										tn.write(b"exit\n")
										hh = tn.read_all().decode('ascii')
										yesdir = hh.splitlines()[8]
										yesdirnzs = hh.splitlines()[7]
										if yesdir == "":
											dslam_adi1 = hh.splitlines()[27]
											success1 = hh.splitlines()[10]
											print (success1)
											a=[dslam_adi1,ipplata,ipport,ipTariff,success1]
											return a
										if yesdirnzs == "":
											dslam_adi1 = hh.splitlines()[26]
											success1 = hh.splitlines()[9]
											print (success1)
											a=[dslam_adi1,ipplata,ipport,ipTariff,success1]
											return a