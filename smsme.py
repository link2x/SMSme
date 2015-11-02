#!/usr/bin/env python

# SMSme - SMS Notification Script
#
#
# Usage from bash:
#     ./smsme.py -m "This is my message." - Sends "This is my message." to the eMail/Phone set up in .smsme
#     ./smsme.py -q                       - Sends "Ping!" with no console output.
#     ./smsme.py -q -d                    - This is just silly. Does nothing.
#
#
# Flags:
#     -m "Message" - Adds a message to send. Default: "Ping!"
#     -d           - Prints to console instead of sending an SMS.
#     -q           - Turns off output.
#
#
# Notes:
#     You should preferably be using App Passwords for this.
#     If you have two-factor authentication, you /must/ use App Passwords.
#
#     This script can also be imported into a python project to quickly add SMS capabilities.
#
#
# Functions:
#     parseArguments() - Automated parsing of supported arguments.
#         You shouldn't use this if you're already handling arguments;
#         instead, set the following variables:
#             .message = str
#             .debug   = bool
#             .quiet   = bool
#
#     loadConfig([file]) - Automated creation/loading of config file.
#         You can skip doing this by setting the following variables:
#             .username    = str
#             .password    = str
#             .fromaddress = str
#             .toaddress   = str
#
#     sendMessage([message]) - Sends a message considering all of the above settings.
#


# Imports
import smtplib      # Sends the eMail->SMS
import os           # Used to check for and/or create a config file
import ConfigParser # Used for our config file
import argparse     # Lets us use arguments

class smsme:
    # Set our variables
    message     = "Ping!"
    debug       = False
    quiet       = True  # We disable output by default
    username    = None
    password    = None
    fromaddress = None
    toaddress   = None
    configfile  = ".smsme"

    def parseArguments(self):# Parse arguments
        parse        = argparse.ArgumentParser()
        parse.add_argument("-m",help="Message to send",type=str)
        parse.add_argument("-d",help="Disable sending SMS",action="store_true")
        parse.add_argument("-q",help="Disable output",action="store_true")
        arguments    = parse.parse_args()
        self.message = arguments.m
        self.debug   = arguments.d
        self.quiet   = arguments.q
        return arguments

    def loadConfig(self, infile = configfile):
        # Load (or create) our config. (./.smsme)
        if not os.path.exists(infile):
            myfile = open(infile,"w")
            myfile.write("[SMSme]\n")
            myfile.write("username:\n")
            myfile.write("password:\n")
            myfile.write("fromaddress:\n")
            myfile.write("toaddress:\n")
            myfile.close()
            if not self.quiet:
                print("Config file "+infile+" created. Please edit it and add the necessary information.")
            raise NoConfig
        else:
            cfg = ConfigParser.ConfigParser()
            cfg.read(infile)
            self.username    = cfg.get("SMSme", "username")
            self.password    = cfg.get("SMSme", "password")
            self.fromaddress = cfg.get("SMSme", "fromaddress")
            self.toaddress   = cfg.get("SMSme", "toaddress")
            if ((not self.username) or (not self.password) or (not self.fromaddress) or (not self.toaddress)):
                if not self.quiet:
                    print("Config file "+infile+" is missing information.")
                raise IncompleteConfig

    def sendMessage(self, msg = None):
        if msg == None:
            msg = self.message
        # Send the eMail->SMS
        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(self.username, self.password)
        server.sendmail(self.fromaddress, self.toaddress, msg)
        server.quit()


# If run directly
if __name__ == "__main__":
    sms = smsme()

    sms.quiet = False

    sms.parseArguments()
    sms.loadConfig()

    if sms.debug:
        if not sms.quiet:
            if sms.message == None:
                sms.message = "Ping!"
            print("Sending "+sms.message+" to "+sms.toaddress)
    else:
        sms.sendMessage()
        if not sms.quiet:
            print("Sent!")
