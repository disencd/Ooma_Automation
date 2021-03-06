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

    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)

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

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # Create UDP transport which listens to any available port
#   transport = lib.create_transport(pj.TransportType.UDP, 
#                                     pj.TransportConfig(0))
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(0))
    print "\nListening on", transport.info().host, 
    print "port", transport.info().port, "\n"
    
    # Start the library
    lib.start()

    #Creating account for Device A
    acc = lib.create_account(pj.AccountConfig("w4f3s.smb.cert1.ooma.com", "q6pw7z12s5", "pdf07vzb91", proxy="sip:w4f3s.smb.cert1.ooma.com;hide"))
    acc_cb = MyAccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    # Creating account for Device B
    acc1 = lib.create_account(pj.AccountConfig("w4f3s.smb.cert1.ooma.com", "en98dpl64c", "anoc9bcowf", proxy="sip:w4f3s.smb.cert1.ooma.com;hide" ))
    acc_cb1 = MyAccountCallback(acc1)
    acc1.set_callback(acc_cb1)
    acc_cb1.wait()

    print "\n"
    print "Registration complete for device A, status=", acc.info().reg_status, \
          "(" + acc.info().reg_reason + ")"

    print "\n"
    print "Registration complete for device A, status=", acc1.info().reg_status, \
          "(" + acc1.info().reg_reason + ")"

    loop_cnt = 0
    while (loop_cnt <= 100):
        loop_cnt+= 1
        # If argument is specified then make call to the URI
        if len(sys.argv) > 1:
            lck = lib.auto_lock()
            current_call = make_call(sys.argv[1])
            print 'Current call is', current_call
            del lck

            my_sip_uri = "sip:" + transport.info().host + \
                         ":" + str(transport.info().port)

            time.sleep(30)

    # Shutdown the library
    transport = None
    acc.delete()
    acc1.delete()
    acc = None
    acc1 = None
    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None

