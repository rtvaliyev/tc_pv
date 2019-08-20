from bs4 import BeautifulSoup
import requests
import telnetlib
import time
import csv


def sellet(usernam,passwor,nomre):
    s = requests.Session()
    data = {
            'txtLogin':usernam,
            'txtPwd':passwor,
            'btnSubmit':'Submit'
            }
    login_request = s.post('http://www.youneededurl/', data=data)
    data1 = {
            'srchLogin':nomre,
            }
    req1 = s.post('http://www.youneededurl/', data=data1)
    soup = BeautifulSoup(req1.text,'html.parser')
    content = soup.find_all('a')
    for links in content:
        link = links['href']
        if "view_user_info&id" in link:
            userlink = 'http://www.youneededurl/'+link
            req2 = s.get(userlink)
            soup1 = BeautifulSoup(req2.text,'html.parser')
            
            try:
                ipdslam = soup1.find('td', text='DSLAM').find_next('td').text.strip()
            except AttributeError:
                ipdslam = soup1.find('td', text='DSLam').find_next('td').text.strip()
            
            try:
                ipplata = soup1.find('td', text='Plate').find_next('td').text.strip()
            except AttributeError:
                ipplata = soup1.find('td', text='Plata').find_next('td').text.strip()
            
            ipport = soup1.find('td', text='Port').find_next('td').text.strip()
            
            try:
                sipport = soup1.find('td', text='Phone').find_next('td').text.strip()
            except AttributeError:
                sipport = soup1.find('td', text='Telefon').find_next('td').text.strip()

            print('  DSLAM  : '+ipdslam)
            print('  PLATA  : '+ipplata)
            print('  PORT   : '+ipport)
            print('  PHONE  : '+sipport)
            with open('hostlar.txt') as txt_file:
                txt_reader = csv.reader(txt_file, delimiter=',')
                for row in txt_reader:
                    if ipdslam==row[0]:
                        if "64portluqhuawei"==row[2]:
                            dslam = row[1]
                            plata = ipplata
                            port = ipport
                            user = "admin"
                            password = "admin"
                            tn = telnetlib.Telnet(dslam)
                            tn.read_until(b">>User name:")
                            tn.write(user.encode('ascii') + b"\n")
                            if password:
                                tn.read_until(b">>User password:")
                                tn.write(password.encode('ascii') + b"\n")
                                tn.write(b"enable\n")
                            time.sleep(1)
                            tn.write(b"display line operation port 0/")
                            tn.write(plata.encode('ascii'))
                            tn.write(b"/")
                            tn.write(port.encode('ascii') + b"\n")
                            tn.write(b"y\n")
                            time.sleep(2)
                            tn.write(b"display mac-address port 0/")
                            tn.write(plata.encode('ascii'))
                            tn.write(b"/")
                            tn.write(port.encode('ascii') + b"\n")
                            # time.sleep(1)
                            tn.read_until(b"#")
                            tn.write(b"quit\n")
                            time.sleep(1)
                            tn.write(b"y\n")
                            output = tn.read_all().decode('ascii')
                            yesdsl = output.splitlines()[2]
                            nodsl = output.splitlines()[5]
                            if yesdsl == "  Are you sure to continue? (y/n)[n]:y":
                                downspeed = output.splitlines()[12]
                                upspeed = output.splitlines()[18]
                                downsnr = output.splitlines()[14]
                                upsnr = output.splitlines()[20]
                                macadres = output.splitlines()[34]
                                boss = output.splitlines()[34]
                                a=[downspeed,upspeed,downsnr,upsnr,macadres,boss]
                                return a
                            if nodsl == "  % Unknown command, the error locates at '^'":
                                deaktivv = output.splitlines()[1]
                                a=[deaktivv]
                                return a
                        try:
                            if "48portluqhuawei"==row[2]:
                                dslam = row[1]
                                plata = ipplata
                                port = ipport
                                user = "admin"
                                password = "admin"
                                tn = telnetlib.Telnet(dslam)
                                tn.read_until(b"Username:")
                                tn.write(user.encode('ascii') + b"\n")
                                if password:
                                    tn.read_until(b"Password:")
                                    tn.write(password.encode('ascii') + b"\n")
                                tn.write(b"enable\n\n")
                                time.sleep(1)
                                tn.write(b"show adsl line state adsl ")
                                tn.write(plata.encode('ascii'))
                                time.sleep(1)
                                tn.write(b"/0/")
                                tn.write(port.encode('ascii') + b"\n")
                                tn.write(b"\n")
                                time.sleep(1)
                                tn.read_until(b"#")
                                time.sleep(1)
                                tn.write(b"exit\n")
                                output = tn.read_all().decode('ascii')
                                yesdsl = output.splitlines()[5]
                                nodsl = output.splitlines()[5]
                                nzsyes = output.splitlines()[4]
                                nzsno = output.splitlines()[4]
                                if yesdsl == "  Current Link Status               : active":
                                    downspeed = output.splitlines()[13]
                                    upspeed = output.splitlines()[20]
                                    downsnr = output.splitlines()[7]
                                    upsnr = output.splitlines()[15]
                                    downatt = output.splitlines()[10]
                                    a=[downspeed,upspeed,downsnr,upsnr,downatt]
                                    return a
                                if nodsl == "  Current Link Status               : activating":
                                    deaktivv = output.splitlines()[5]
                                    a=[deaktivv]
                                    return a
                                if nzsyes == "  Current Link Status               : active":
                                    downspeed = output.splitlines()[12]
                                    upspeed = output.splitlines()[19]
                                    downsnr = output.splitlines()[6]
                                    upsnr = output.splitlines()[14]
                                    downatt = output.splitlines()[9]
                                    a=[downspeed,upspeed,downsnr,upsnr,downatt]
                                    return a
                                if nzsno == "  Current Link Status               : activating":
                                    deaktivv = output.splitlines()[4]
                                    a=[deaktivv]
                                    return a
                            if "iskrateladsl"==row[2]:
                                dslam = row[1]
                                plata = ipplata
                                port = ipport
                                user = "admin"
                                password = "admin"
                                tn = telnetlib.Telnet(dslam)
                                tn.read_until(b"user id :")
                                tn.write(user.encode('ascii') + b"\n")
                                if password:
                                    tn.read_until(b"password:")
                                    tn.write(password.encode('ascii') + b"\n")
                                time.sleep(1)
                                tn.write(b"show dsl port ")
                                time.sleep(1)
                                tn.write(port.encode('ascii') + b"\n")
                                time.sleep(1)
                                tn.read_until(b"mBAN>")
                                time.sleep(1)
                                tn.write(b"exit\n")
                                output = tn.read_all().decode('ascii')
                                yesdsl = output.splitlines()[9]
                                nodsl = output.splitlines()[9]
                                if yesdsl == "DSL State                      Active":
                                    duspeed = output.splitlines()[11]
                                    dusnr = output.splitlines()[13]
                                    a=[duspeed,dusnr]
                                    return a
                                if nodsl == "DSL State                      Handshake":
                                    deaktivv = output.splitlines()[8]
                                    a=[deaktivv]
                                    return a
                        except IndexError:
                            return None
                        try:
                            if "iskratelvdsl"==row[2]:
                                dslam = row[1]
                                plata = ipplata
                                port = ipport
                                port = int(port)
                                if port<65 and port>0:
                                    port = str(port)
                                user = "admin"
                                password = "admin"
                                showdsl = "show dsl port current values 0/"
                                quiting = "quit\r"
                                nosaving = "n"
                                enter = "\r"
                                tn = telnetlib.Telnet(dslam)
                                tn.read_until(b"(none) login: ")
                                tn.write(user.encode('ascii') + b"\r")
                                if password:
                                    tn.read_until(b"Password:")
                                    tn.write(password.encode('ascii') + b"\r")
                                tn.read_until(b"#")
                                tn.write(showdsl.encode('ascii'))
                                tn.write(port.encode('ascii') + b"\r")
                                time.sleep(1)
                                tn.read_until(b"Admin state:")
                                tn.write(b"\t")
                                time.sleep(1)
                                tn.write(quiting.encode('ascii'))
                                time.sleep(1)
                                tn.write(nosaving.encode('ascii'))
                                time.sleep(1)
                                tn.write(enter.encode('ascii'))
                                output = tn.read_all().decode('ascii')
                                yesdsl = output.splitlines()[2]
                                nodsl = output.splitlines()[2]
                                if yesdsl == "Operational state:    Active - Showtime L0":
                                    duspeed = output.splitlines()[31]
                                    dusnr = output.splitlines()[41]
                                    empt = output.splitlines()[40]
                                    a=[duspeed,dusnr,empt]
                                    return a
                                if nodsl == "Operational state:    Quiet":
                                    deaktivv = output.splitlines()[20]
                                    a=[deaktivv]
                                    return a
                        except(AttributeError,ValueError):
                            return None
                        try:
                            if "iskratelvdsl32"==row[2]:
                                dslam = row[1]
                                plata = ipplata
                                port = ipport
                                port = int(port)
                                if port<33 and port>0:
                                    port = str(port)
                                user = "admin"
                                password = "admin"
                                showdsl = "show dsl port current values 0/"
                                quiting = "quit\r"
                                nosaving = "n"
                                enter = "\r"
                                tn = telnetlib.Telnet(dslam)
                                tn.read_until(b"(none) login: ")
                                tn.write(user.encode('ascii') + b"\r")
                                if password:
                                    tn.read_until(b"Password:")
                                    tn.write(password.encode('ascii') + b"\r")
                                tn.read_until(b"#")
                                tn.write(showdsl.encode('ascii'))
                                tn.write(port.encode('ascii') + b"\r")
                                tn.read_until(b"Admin state:")
                                tn.write(b"\t")
                                time.sleep(1)
                                tn.write(quiting.encode('ascii'))
                                time.sleep(1)
                                tn.write(nosaving.encode('ascii'))
                                time.sleep(1)
                                tn.write(enter.encode('ascii'))
                                output = tn.read_all().decode('ascii')
                                yesdsl = output.splitlines()[2]
                                nodsl = output.splitlines()[2]
                                if yesdsl == "Operational state:    Active - Showtime L0":
                                    duspeed = output.splitlines()[24]
                                    dusnr = output.splitlines()[34]
                                    empt = output.splitlines()[33]
                                    a=[duspeed,dusnr,empt]
                                    return a
                                if nodsl == "Operational state:    Quiet":
                                    deaktivv = output.splitlines()[13]
                                    a=[deaktivv]
                                    return a
                        except(AttributeError,ValueError):
                            return None

                        if "raisecom"==row[2]:
                            dslam = row[1]
                            plata = ipplata
                            port = ipport
                            port = int(port)
                            if port<29 and port>0:
                                port = str(port)
                            else:
                                a = None
                                return a
                            user = "admin"
                            password = "admin"
                            try:
                                tn = telnetlib.Telnet(dslam)
                            except:
                                switchdown = "'switch'-lə əlaqə yoxdur!"
                                a=[switchdown,switchdown,switchdown,switchdown]
                                return a
                            tn.read_until(b"Login:")
                            tn.write(user.encode('ascii') + b"\n")
                            if password:
                                tn.read_until(b"Password:")
                                tn.write(password.encode('ascii') + b"\n")
                            time.sleep(1)
                            tn.write(b"show interface port  ")
                            tn.write(port.encode('ascii') + b"\n")
                            time.sleep(1)
                            tn.write(b"show mac-address-table l2-address port ")
                            tn.write(port.encode('ascii') + b"\n")
                            time.sleep(1)
                            tn.read_until(b"#")
                            tn.write(b"exit\n")
                            time.sleep(1)
                            output = tn.read_all().decode('ascii')
                            mac = output.splitlines()[6][14:16]
                            machit = output.splitlines()[11][42:46]
                            if mac == "up" and machit == "Hit":
                                portupordown = output.splitlines()[6]
                                macaddres = output.splitlines()[11]
                                hostunadi = output.splitlines()[12]
                                boss1 = output.splitlines()[11]
                                a=[portupordown,macaddres,hostunadi,boss1]
                                return a
                            else:
                                portupordown = output.splitlines()[6]
                                macaddres = output.splitlines()[10]
                                hostunadi = output.splitlines()[11]
                                boss1 = output.splitlines()[11]
                                a=[portupordown,macaddres,hostunadi,boss1]
                                return a

                        if "edge-core"==row[2]:
                            dslam = row[1]
                            plata = ipplata
                            port = ipport
                            port = int(port)
                            if port<29 and port>0:
                                port = str(port)
                            else:
                                a = None
                                return a
                            user = "admin"
                            password = "admin"
                            try:
                                tn = telnetlib.Telnet(dslam)
                            except:
                                switchdown = "'switch'-lə əlaqə yoxdur!"
                                boss1 = None
                                a=[switchdown,switchdown,switchdown,switchdown,boss1,boss1,boss1]
                                return a
                            tn.read_until(b"Username:")
                            tn.write(user.encode('ascii') + b"\n")
                            if password:
                                tn.read_until(b"Password:")
                                tn.write(password.encode('ascii') + b"\n")
                            time.sleep(1)
                            tn.write(b"show system" + b"\n\t")
                            time.sleep(1) 
                            tn.write(b"show interfaces status ethernet 1/")
                            tn.write(port.encode('ascii') + b"\n ")
                            time.sleep(1)
                            tn.write(b"show mac-address-table interface ethernet 1/")
                            tn.write(port.encode('ascii') + b"\n")
                            tn.write(b"show mac-address-table interface ethernet 1/")
                            tn.write(port.encode('ascii') + b"\n")
                            time.sleep(1)
                            tn.read_until(b"#")
                            tn.write(b"exit\n")
                            output = tn.read_all().decode('ascii')
                            version = output.splitlines()[1][18:]
                            if version == " : ES3528MV2":
                                macdelete = output.splitlines()[58][:3]
                                if macdelete == "Vty":
                                    portactordeact = output.splitlines()[34][27:]
                                    portupordown = output.splitlines()[48][27:]
                                    portduplex = output.splitlines()[50][27:]
                                    macaddres = output.splitlines()[60][11:-32]
                                    hostunadi = output.splitlines()[5][26:]
                                    boss1 = None
                                    a=[portupordown,macaddres,hostunadi,portactordeact,portduplex,boss1,boss1]
                                    return a
                                else:
                                    portactordeact = output.splitlines()[34][27:]
                                    portupordown = output.splitlines()[48][27:]
                                    portduplex = output.splitlines()[50][27:]
                                    macaddres = output.splitlines()[58][11:-32]
                                    hostunadi = output.splitlines()[5][26:]
                                    boss1 = None
                                    a=[portupordown,macaddres,hostunadi,portactordeact,portduplex,boss1,boss1]
                                    return a
                            if version == ": Edge-Core FE L2 Switch ES3528M":
                                macdelete = output.splitlines()[51][:3]
                                if macdelete == "Vty":
                                    portactordeact = output.splitlines()[23][26:]
                                    portupordown = output.splitlines()[43][26:]
                                    portduplex = output.splitlines()[45][26:]
                                    macaddres = output.splitlines()[50][11:28]
                                    hostunadi = output.splitlines()[5][26:]
                                    boss1 = None
                                    a=[portupordown,macaddres,hostunadi,portactordeact,portduplex,boss1,boss1]
                                    return a
                                else:
                                    portactordeact = output.splitlines()[23][26:]
                                    portupordown = output.splitlines()[43][26:]
                                    portduplex = output.splitlines()[45][26:]
                                    macaddres = output.splitlines()[51][11:28]
                                    hostunadi = output.splitlines()[5][26:]
                                    boss1 = None
                                    a=[portupordown,macaddres,hostunadi,portactordeact,portduplex,boss1,boss1]
                                    return a
                            if version == " : ES3510MAv2":
                                macdelete = output.splitlines()[49][2:5]
                                if macdelete == "Eth":
                                    portactordeact = output.splitlines()[23][27:]
                                    portupordown = output.splitlines()[39][27:]
                                    portduplex = output.splitlines()[41][27:]
                                    macaddres = output.splitlines()[49][11:-32]
                                    hostunadi = output.splitlines()[5][26:]
                                    boss1 = None
                                    a=[portupordown,macaddres,hostunadi,portactordeact,portduplex,boss1,boss1]
                                    return a
                                else:
                                    portactordeact = output.splitlines()[23][27:]
                                    portupordown = output.splitlines()[39][27:]
                                    macaddres = output.splitlines()[49][11:-32]
                                    hostunadi = output.splitlines()[5][26:]
                                    boss1 = None
                                    a=[portupordown,macaddres,hostunadi,portactordeact,boss1,boss1,boss1]
                                    return a
