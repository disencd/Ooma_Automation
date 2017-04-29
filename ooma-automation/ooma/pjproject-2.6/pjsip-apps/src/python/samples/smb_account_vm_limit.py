# $Id: call.py 2171 2008-07-24 09:01:33Z bennylp $
#
# SIP call sample.
#
# Copyright (C) 2003-2008 Benny Prijono <benny@prijono.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
#
import sys
import pjsua as pj
import threading
import time

LOG_LEVEL=3
current_call = None

# Logging callback
def log_cb(level, str, len):
    print str,


# Callback to receive events from account
class MyAccountCallback(pj.AccountCallback):
     sem = None

     def __init__(self, account):
        pj.AccountCallback.__init__(self, account)

     def wait(self):
       	self.sem = threading.Semaphore(0)
        self.sem.acquire()

     def on_reg_state(self):
        if self.sem:
           if self.account.info().reg_status >= 200:
               self.sem.release()
     
    # Notification on incoming call
     def on_incoming_call(self, call):
        global current_call 
        if current_call:
            call.answer(486, "Busy")
            return
            
        print "Incoming call from ", call.info().remote_uri
        print "Press 'a' to answer"

        current_call = call

        call_cb = MyCallCallback(current_call)
        current_call.set_callback(call_cb)

        current_call.answer(180)

       
# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):

    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
        global current_call
        print "Call with", self.call.info().remote_uri,
        print "is", self.call.info().state_text,
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
        
        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            print 'Current call is', current_call

    # Notification when call's media state has changed.
    def on_media_state(self):
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            pj.Lib.instance().conf_connect(call_slot, 0)
            pj.Lib.instance().conf_connect(0, call_slot)
            print "Media is now active"
        else:
            print "Media is inactive"



# Function to make call
def make_call(uri):
    try:
        print "Making call to", uri
        return acc.make_call(uri, cb=MyCallCallback(),hdr_list=None)
    except pj.Error, e:
        print "Exception: " + str(e)
        return None
        

# Create library instance
lib = pj.Lib()

try:
    # Init library with default config and some customized
    # logging config.
    lib.init(log_cfg = pj.LogConfig(level=LOG_LEVEL, callback=log_cb))
    lib.set_null_snd_dev() 
    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(0))
    print "\nListening on", transport.info().host, 
    print "port", transport.info().port, "\n"
    
    # Start the library
    lib.start()

    #Creating account for Device A
    acc = lib.create_account(pj.AccountConfig("2wfcg.smb.sandbox.ooma.com", "7goi8mbbyb", "y1kygj5lpi", proxy="sip:2wfcg.smb.sandbox.ooma.com;hide")) 
    acc_cb = MyAccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    my_sip_uri = "sip:" + transport.info().host + \
                 ":" + str(transport.info().port)

    cnt = 1
    print "My SIP URI is", my_sip_uri
    # Menu loop
    while True:

        if current_call:
            continue
        lck = lib.auto_lock()
        print my_sip_uri,  " is calling " , sys.argv[1] , " for " , cnt , "th time\n"
        cnt += 1
        current_call = make_call(sys.argv[1])
        del lck

        time.sleep(30)

        if not current_call:
            print "There is no call"
            continue
        current_call.hangup()

    # Shutdown the library
    transport = None
    acc.delete()
    acc = None
    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None

