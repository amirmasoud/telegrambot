# -*- coding: utf-8 -*-
from pytg.receiver import Receiver
from pytg.sender import Sender
from pytg.utils import coroutine
import json
import requests
import time;
import sqlite3


conn = sqlite3.connect('./db.sqlite')
c = conn.cursor()

@coroutine
def receive_listener(receiver):
    try:
        while True:
            msg = (yield)
				# if(msg.event == "message" and msg.sender.username != "doorbash"):
				# 	sender.send_msg("@" + msg.sender.username,msg.text)
				# 	print(msg)
    except KeyboardInterrupt:
        receiver.stop()
        print("Exiting")


if __name__ == '__main__':
    receiver = Receiver(port=4458,host="localhsot")  # get a Receiver Connector instance
    sender = Sender(port=4458,host="localhost")

    session = requests.Session()
    session.headers.update({"User-Agent":"Dalvik/2.1.0 (Linux; U; Android 4.0.0)" , "Accept-Encoding" : "gzip"})

    while(True):
        try:
            r = session.get("http://app.bartarinha.ir/fa/webservice/json/news/service/20/1")
            if(r.status_code == 200):
                records = json.loads(r.text)
                for record in records:
                    if record['hits'] > 200:
                        try:
                            c.execute("INSERT INTO records (id) VALUES (" + record['record_id'] + ")")
                            conn.commit()
                            sender.send_msg('@hot_news_fa',record['title'] + '\n\n' + record['subtitle'] + '\n\n' + 'https://telegram.me/joinchat/BVzZhT8QRD7mxs7mr8_0vA')
                        except sqlite3.IntegrityError:
                            pass
        except Exception:
            pass

        time.sleep(120)
        conn.close()
        
    # receiver.start()
    # receiver.message(receive_listener(receiver))
    # receiver.stop()