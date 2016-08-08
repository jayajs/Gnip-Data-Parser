'''
Created on Jan 19, 2016

@author: user
'''
from time import sleep
from threading import Thread
from product.com.src.live import Collector
from product.com.src.est import Test


def some_task():
    collect = Collector.StdOutListener()
    collect.run()


t = Thread(target=some_task)  
# run the some_task function in another
# thread
t.daemon = True               
# Python will exit when the main thread
# exits, even if this thread is still
# running
t.start()
snooziness = int(100)
sleep(snooziness)
tst = Test()
tst.run( )