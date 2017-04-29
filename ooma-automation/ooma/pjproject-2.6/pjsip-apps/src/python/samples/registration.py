# $Id: registration.py 2171 2008-07-24 09:01:33Z bennylp $
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

#qtxpi.smb.cert1.ooma.com
#d0hxqab707
#nrot181sxm

#username : w4f3s.smb.cert1.ooma.com
#username : qc41lb8o08
#password : netc19kcs9

##############################
#TLS
##############################
#realm : nagpn.smb.cert1.ooma.com
#username : fj4cdew1yi
#password : cssljvix46

import sys
import pjsua as pj
import threading


def log_cb(level, str, len):
    print str,

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

lib = pj.Lib()

try:
    lib.init(log_cfg = pj.LogConfig(level=4, callback=log_cb))
    lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5080))
    #lib.create_transport(pj.TransportType.TLS, pj.TransportConfig(5080))
    lib.start()
    #acc = lib.create_account(pj.AccountConfig("w4f3s.smb.cert1.ooma.com", "qc41lb8o08", "netc19kcs9"))
    acc = lib.create_account(pj.AccountConfig("w4f3s.smb.cert1.ooma.com", "fj4cdew1yi", "cssljvix46"))
    #acc = lib.create_account(pj.AccountConfig("sbc1-cert1-ext.cn.ooma.com", "disen", "netc19kcs9"))

    acc_cb = MyAccountCallback(acc)
    acc.set_callback(acc_cb)
    acc_cb.wait()

    print "\n"
    print "Registration complete, status=", acc.info().reg_status, \
          "(" + acc.info().reg_reason + ")"
    print "\nPress ENTER to quit"
    sys.stdin.readline()

    lib.destroy()
    lib = None

except pj.Error, e:
    print "Exception: " + str(e)
    lib.destroy()

