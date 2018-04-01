# encoding: utf8
# Burp extension for the 'Wawacoin' NDH 2018 quals challenge
# Write-up: https://tipi-hack.github.io/2018/04/01/quals-NDH-18-Wawacoin.html
# By Clément Notin @cnotin
# Based on HTTPInjector by @Agarri_FR:
# http://www.agarri.fr/kom/archives/2013/10/22/exploiting_wpad_with_burp_suite_and_the_http_injector_extension/index.html

from burp import IBurpExtender
from burp import IHttpListener
import subprocess


class BurpExtender(IBurpExtender, IHttpListener):
    def registerExtenderCallbacks(self, callbacks):
        self._helpers = callbacks.getHelpers()

        callbacks.setExtensionName("NDH quals")

        callbacks.registerHttpListener(self)

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        # only process requests
        if not messageIsRequest:
            return

        req = messageInfo.getRequest()
        req = self._helpers.bytesToString(req)

        if "session=" not in req:
            return
        if "GET /static" in req:
            return

        session = req.split("session=")[1].split("\r\n")[0]
        print "session before=" + session

        output = subprocess.check_output(["/root/tools/hash_extender/hash_extender",
                                          "--data", "user=demo",
                                          "--signature", "9183ff6055a46981f2f71cd36430ed3d9cbf6861",
                                          "--format", "sha1",
                                          "--secret", "16",
                                          "--append", session
                                          ])
        sig = output.split("New signature: ")[1].split("\n")[0]
        data = output.split("New string: ")[1].split("\n")[0]

        session_new = "%s|%s" % (data, sig)
        print "session after =" + session_new

        req = req.replace(session, session_new)

        req = self._helpers.stringToBytes(req)

        messageInfo.setComment("payload %s" % session)
        messageInfo.setHighlight("yellow")

        messageInfo.setRequest(req)
