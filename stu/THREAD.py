# coding=utf-8
#
# 首先导入threading 模块，这是使用多线程的前提。
import threading
from time import ctime, sleep


def music(name):
    for i in range(2):
        print("I was listening to music . %s %s" % (name, ctime()))
        sleep(1)


def coding(code):
    for i in range(2):
        print("I was coding codes! %s %s" % (code, ctime()))
        sleep(5)


threads = []

# 创建了threads数组，创建线程t1,使用threading.Thread()方法，
# 在这个方法中调用music方法target=music，args方法对music进行传参。 把创建好的线程t1装到threads数组中。
# 定义单元素的tuple有歧义，所以 Python 规定，单元素 tuple 要多加一个逗号“,”，这样就避免了歧义：
threads.append(threading.Thread(target=music, args=(u'伟大的闯爷之歌2',)))
threads.append(threading.Thread(target=music, args=(u'伟大的闯爷之歌',)))
threads.append(threading.Thread(target=music, args=(u'伟大的闯爷之歌3',)))
# 接着以同样的方式创建线程t2，并把t2也装到threads数组。


threads.append(threading.Thread(target=coding, args=(u'python代码3',)))
threads.append(threading.Thread(target=coding, args=(u'python代码2',)))
threads.append(threading.Thread(target=coding, args=(u'python代码1',)))

if __name__ == '__main__':
    for t in threads:

        # setDaemon(True)将线程声明为守护线程，必须在start() 方法调用之前设置，如果不设置为守护线程程序会被无限挂起。
        # 子线程启动后，父线程也继续执行下去，
        # 当父线程执行完最后一条语句print "all over %s" %ctime()后，没有等待子线程，直接就退出了，同时子线程也一同结束。
        t.setDaemon(True);
        # 开始线程活动
        t.start()

    print(" all over %s" % ctime())

