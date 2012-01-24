import signal
import os
import time
import urllib

from simplejson import dumps as to_json
from simplejson import loads as from_json

from webgui import start_gtk_thread
from webgui import launch_browser
from webgui import synchronous_gtk_message
from webgui import asynchronous_gtk_message
from webgui import kill_gtk_thread
 
from db import *

class Global(object):
    quit = False
    @classmethod
    def set_quit(cls, *args, **kwargs):
        cls.quit = True


def main():
    start_gtk_thread()
    
    langcard_db = LangcardDB();

    # Create a proper file:// URL pointing to demo.xhtml:
    file = os.path.abspath('demo.xhtml')
    uri = 'file://' + urllib.pathname2url(file)
    browser, web_recv, web_send = \
        synchronous_gtk_message(launch_browser)(uri,
                                                quit_function=Global.set_quit)

    # Finally, here is our personalized main loop, 100% friendly
    # with "select" (although I am not using select here)!:
    last_second = time.time()
    uptime_seconds = 1
    clicks = 0
    while not Global.quit:
        # GETLIST
        # SETPHRA
        current_time = time.time()
        again = False
        msg = web_recv()

        if msg:
            print msg

        if msg and msg[0:7]=="SETPHRA":
            msg = from_json(msg[7:])
            langcard_db.langcardSetPhrase(msg);
            again = True
            continue

        if msg and msg[0:7]=="GETLIST":
            phrases = langcard_db.langcardGetPhraseList()
            previd=-1
            phraselist = {}

            for index in phrases:
                currentid=phrases[index][0]

                if (currentid!=previd):

                    phrase = {}
                    phrase['id'] = phrases[index][0]
                    phrase['phrase'] = phrases[index][4]
                    phrase['words'] = {}

                word = {}
                word['original'] = phrases[index][2];
                word['translation'] = phrases[index][3];
                word['comments'] = phrases[index][1];
                word['position'] = phrases[index][5];

                phrase['words'][len(phrase['words'])] = word;

                if (currentid!=previd):
                    phraselist[len(phraselist)] = phrase
              
                previd=currentid;

#            phraselist[len(phraselist)] = phrase
            phraselist = to_json(phraselist)

            phraselist = phraselist.replace('\'','')
            web_send("setList('%s')" % (phraselist));

        if again: pass
        else:     time.sleep(0.1)


def my_quit_wrapper(fun):
    signal.signal(signal.SIGINT, Global.set_quit)
    def fun2(*args, **kwargs):
        try:
            x = fun(*args, **kwargs) # equivalent to "apply"
        finally:
            kill_gtk_thread()
            Global.set_quit()
        return x
    return fun2


if __name__ == '__main__': # <-- this line is optional
    my_quit_wrapper(main)()
