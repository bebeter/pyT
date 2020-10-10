# coding utf8
import queue
import threading
import urllib.request
import time
import common
import os
import fbsj_file

dms = []

queue = queue.Queue()


def creatUrl(rq):
    f = open(common.dm_txt, "r")
    lines = f.readlines()
    for dm in lines:
        downstr = "http://market.finance.sina.com.cn/downxls.php?date=2013-07-08&symbol=" + marketstr(dm)
        dms.append(downstr)

# 读取需处理的代码
def readdm():
    f = open(common.dm_txt, "r")
    lines = f.readlines()
    for line in lines:
        dms.append(line.split("\t")[0].strip())

    f.close()


def marketstr(dm):
    # print dm,dm[0]
    if dm[0] == str(6):
        dm = 'sh' + dm
    elif dm[0] == str(3) or dm[0] == str(0):
        dm = 'sz' + dm
    # print dm
    return dm


class ThreadUrl(threading.Thread):
    def __init__(self, queue,dirs):
        threading.Thread.__init__(self)
        self.queue = queue
        self.dirs = dirs

    def getRq(self, dm):
        f = open(common.base_diretory + "\\TXTDAY\\" + marketstr(dm) + ".txt", "r")
        rq = []
        for line in f.readlines():
            daydata = line[:-1].split(",")
            rq.append(daydata[0].replace("/", "-"))
        f.close()
        return rq

    def run(self):
        while True:
            # grabs host from queue
            # print (dd)
            dm = self.queue.get()
            for dir in self.dirs:
                try:

                    # print (url.read())
                    fbdir = common.base_diretory + "\\level2\\" + dir + "\\"
                    filename = fbdir + dm + ".txt"
                    #f = open(filename, "w")
                    #fbsj_file.deal_gp_fb(filename, dir, dm)
                    #f.write(data)

                    print("deal  "+ filename+"  done "   )

                except:
                    print(filename, "not exist")
                    pass
            # signals to queue job is done
            self.queue.task_done()


start = time.time()


def main():
    '''
    print(len(common.rq_index), common.rq_index[-5:])
    for down_rq in common.rq_index[-100:]:
        print(down_rq)
    '''
    '''
        fsdir = common.base_diretory + "\\sina\\" + down_rq + "\\"
        if (not os.path.exists(fsdir)):
            print("not exist...", fsdir)
            os.mkdir(fsdir)
    '''

    print("hahah")
    readdm()
    # dms.append("002079")
    # dms.append("002340")
    # dms.append("000917")
    # dms.append("600388")
    for dm in dms:
        # print "h:",dm
        queue.put(dm)
    print("h:")


    dirs= ["201208","201209"]


    # spawn a pool of threads, and pass them queue instance
    for i in range(10):
        t = ThreadUrl(queue,dirs)
        t.setDaemon(True)
        t.start()

    # wait on the queue until everything has been processed
    queue.join()



main()

'''
readdm()
for dm in dms:
    print(dm)
'''

print("Elapsed Time: %s" % (time.time() - start))
