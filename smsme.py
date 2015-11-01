#!/usr/bin/env python
#
# SMSme - SMS Notification Script
#
#
# Usage:
# ./smsme.py -m "This is my message."
#
#
# Flags:
# -m "Message" - Adds a message to send. Default: "Ping!"
# -d           - Prints to console instead of sending an SMS.
#

# Imports
import smtplib  # Sends the eMail->SMS
import os # Used to check for and/or create a config file
import ConfigParser # Used for our config file
import argparse # Lets us use arguments

# Set our variables
username    = None
password    = None

fromaddress = None
toaddress   = None

message     = None
debug       = False

configfile  = ".smsme"

# Load (or create) our config. (./.smsme)
if not os.path.exists(configfile):
    myfile = open(configfile,"w")
    myfile.write("[SMSme]\n")
    myfile.write("username:\n")
    myfile.write("password:\n")
    myfile.write("fromaddress:\n")
    myfile.write("toaddress:\n")
    myfile.close()
    print("Config file .smsme created.")
else:
    cfg = ConfigParser.ConfigParser()
    cfg.read(configfile)
    username    = cfg.get("SMSme","username")
    password    = cfg.get("SMSme","password")
    fromaddress = cfg.get("SMSme","fromaddress")
    toaddress   = cfg.get("SMSme","toaddress")

# Parse arguments
parse       = argparse.ArgumentParser()
parse.add_argument("-m",help="Message to send",type=str)
parse.add_argument("-d",help="Disable sending SMS",action="store_true")
arguments   = parse.parse_args()

# Get our message
message = arguments.m
debug   = arguments.d

if (message == None): # If no message was specified, just ping me.
    message     = "Ping!"

# Debug stuff
if (debug == True):
    print(username+" is sending '"+message+"' to "+toaddress)


# Send the eMail->SMS
if (debug != True):
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddress, toaddress, message)
    server.quit()

# Feedback
print("Sent!")
