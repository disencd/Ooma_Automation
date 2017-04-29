# $Id: simplecall.py 2171 2008-07-24 09:01:33Z bennylp $
#
# SIP account and registration sample. In this sample, the program
# will block to wait until registration is complete
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
import wave
import time


# Logging callback
def log_cb(level, str, len):
    print str,


# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):
    def __init__(self, call=None):
        pj.CallCallback.__init__(self, call)

    # Notification when call state has changed
    def on_state(self):
	global current_call
	global in_call
        global lib
        print "Call is ", self.call.info().state_text,
        print "last code =", self.call.info().last_code,
        print "(" + self.call.info().last_reason + ")"
        #if self.call.info().state == pjsua.CallState.DISCONNECTED:
        if self.call.info().state == pj.CallState.DISCONNECTED:
            current_call = None
            print 'Current call is', current_call

            in_call = False
        #elif self.call.info().state == pjsua.CallState.CONFIRMED:
        elif self.call.info().state == pj.CallState.CONFIRMED:
            # Call is Answred
            print "Call Answred"
            wfile = wave.open("message.wav")
            w_time = (1.0 * wfile.getnframes()) / wfile.getframerate()
            print str(w_time) + "ms"
            wfile.close()
            call_slot = self.call.info().conf_slot
            self.wav_player_id = lib.instance().create_player('message.wav', loop=False)
            self.wav_slot = lib.instance().player_get_slot(self.wav_player_id)
            lib.instance().conf_connect(self.wav_slot, call_slot)
            time.sleep(50)
            lib.instance().player_destroy(self.wav_player_id)
            self.call.hangup()
	    in_call = False

    # Notification when call's media state has changed.
    def on_media_state(self):
        global lib
        if self.call.info().media_state == pj.MediaState.ACTIVE:
            # Connect the call to sound device
            call_slot = self.call.info().conf_slot
            lib.conf_connect(call_slot, 0)
            lib.conf_connect(0, call_slot)
            print "Hello world, I can talk!"


# Check command line argument
if len(sys.argv) != 2:
    print "Usage: simplecall.py <dst-URI>"
    sys.exit(1)

try:
    # Create library instance
    lib = pj.Lib()

    # Init library with default config
    lib.init(log_cfg=pj.LogConfig(level=3, callback=log_cb))

    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP)

    # Start the library
    lib.start()

    # Create UDP transport which listens to any available port
    transport = lib.create_transport(pj.TransportType.UDP)

    # Create local/user-less account
    acc = lib.create_account_for_transport(transport)
    lib.set_codec_priority("SPEEX/8000/1", 0)
    lib.set_codec_priority("SPEEX/16000/1", 0)
    lib.set_codec_priority("SPEEX/32000/1", 0)
    lib.set_codec_priority("iLBC/8000/1", 0)
    lib.set_codec_priority("GSM/8000/1", 0)
    loop_cnt = 0
    while (loop_cnt <= 1000):
        loop_cnt += 1
        # If argument is specified then make call to the URI
        if len(sys.argv) > 1:
            lck = lib.auto_lock()
            # Make call
            call = acc.make_call(sys.argv[1], MyCallCallback())
            del lck

            my_sip_uri = "sip:" + transport.info().host + \
                         ":" + str(transport.info().port)
            print "\nCall No - ", loop_cnt

        time.sleep(13)
        call.hangup()
        # Shutdown the library
        time.sleep(3)

    acc.delete()
    time.sleep(3)

    transport = None

    # Wait for ENTER before quitting
    print "Press <ENTER> to quit"
    input = sys.stdin.readline().rstrip("\r\n")

    # We're done, shutdown the library
    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()
    lib = None
    sys.exit(1)

