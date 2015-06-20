#! /usr/bin/python

from pylibftdi import BitBangDevice
import os
import time
import threading


ports=[
        {'name':'modem','status':'ON'},
        {'name':'firewall','status':'ON'},
        {'name':'none','status':'ON'},
        {'name':'none','status':'ON'},
        {'name':'none','status':'ON'},
        {'name':'none','status':'ON'},
        {'name':'none','status':'ON'},
        {'name':'none','status':'ON'},
        ]

pingIP = "8.8.8.8"

bb = BitBangDevice()

def main():
        #print "Running IN MAIN"
        status = ping()
        #print status

        if(status == 'DOWN'):
                recoverModem()
        else:
                threading.Timer(60,main,args=[]).start()

def recoverModem():
        os.system("date")
        print "Recovering Modem.. Checking Status Again"
        status = ping()
        print status

        if(status == 'DOWN'):
                print "Resetting Modem"
                setstatus('modem','OFF')
                time.sleep(10)
                setstatus('modem','ON')
                print "Waiting for modem to reset..."
                time.sleep(300)
                recoverFirewall()
        else:
                threading.Timer(60,main,args=[]).start()
def recoverFirewall():
        os.system("date")
        print "Recovering Firewall.. Checking Status Again"
        status = ping()
        print status

        if(status == 'DOWN'):
                print "Resetting Modem and Firewall.."
                setstatus('firewall','OFF')
                setstatus('modem','OFF')
                time.sleep(10)
                setstatus('firewall','ON')
                setstatus('modem','ON')
                print "Waiting for Modem and Firewall to come back up.. "
                time.sleep(600)
                recoverModem()
        else:
                threading.Timer(60,main,args=[]).start()



def ping():
        status = os.system("ping -c 1 " + pingIP + " > /dev/null")
        if(status == 0):
                status = "UP"
        else:
                status = "DOWN"

        return status


def formdata():
        global ports
        datatosend = ""
        for x in reversed(range(0,8)):
                #print ports[x]['status']
                if ports[x]['status'] == 'OFF':
                        datatosend = datatosend + "1"
                else:
                         datatosend = datatosend + "0"
        return datatosend

def setstatus(item,status):
        global ports
        global bb
        for x in range(0,8):
                if ports[x]['name'] == item:
                        ports[x]['status'] = status
        senddata()

def senddata():
        bb.port = int(formdata(),2)

if __name__ == '__main__':
        main()
