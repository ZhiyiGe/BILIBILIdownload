from tkinter import *

import requests
import re
import sys
from you_get import common as you_get
from tkinter.filedialog import askdirectory


class BilibiliDownloader(object):
    def __init__(self):
        pass

    @staticmethod
    def run(dic, urll, kstart=None):
        # kstart is the last number printed on the screen.
        k = 0
        kt = len(urll)
        for u in urll:
            k += 1
            if kstart:
                if k <= kstart:
                    continue
            try:
                sys.argv = ['you-get', '-o', dic, u]
                you_get.main()
            except Exception as e:
                print(e)
                print('*Loss one. The url is:{}'.format(u))
            print('{}/{} done.'.format(k, kt))
        return


class BilibiliVideoManager(object):

    def __init__(self):
        self.rule = re.compile('<span class="cur-page">.*?/(.*?)</span></div>', re.S)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        self.trule = re.compile('eta="true">(.*?)_哔哩哔哩', re.S)
        self.alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'

    # 根据第一个视频的url和视频总页数获得所有视频的url并以列表形式返回
    @staticmethod
    def genurl(url, page):
        urls = []
        urls.append(url)
        for idx in range(1, page):
            urls.append('{}?p={}'.format(url, idx + 1))
        return urls

    # bv号 转 av号
    @staticmethod
    def bv2av(x):
        table = "fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF"
        tr = {}
        for i in range(58):
            tr[table[i]] = i
        s = [11, 10, 3, 8, 4, 6]
        xor = 177451812
        add = 8728348608
        r = 0
        for i in range(6):
            r += tr[x[s[i]]] * 58 ** i
        return (r - add) ^ xor

    # 以列表的形式返回视频的Url
    def run(self, vid, mode='av'):  # av91882697 av
        print(mode)
        # bv 转 av
        if mode == 'BV':
            vid = 'av' + str(self.bv2av(vid))
            print(vid)

        url = 'https://www.bilibili.com/video/{}'.format(vid)
        print(url)
        #      https://www.bilibili.com/video/av91882697
        req = requests.get(url, headers=self.headers)
        content = str(req.content, 'utf8')
        wholep = self.rule.findall(content)  # 视频总个数
        if wholep:  # 若得到了页数则执行
            return self.genurl(url, int(wholep[0]))
        return [url, ]

    # 获取视频名
    def gettitle(self, url):
        c = str(requests.get(url, headers=self.headers).content, 'utf8')
        title = self.trule.findall(c)[0]
        return title


class Manager(object):
    def __init__(self, master):
        self.bd = BilibiliDownloader()
        self.bvm = BilibiliVideoManager()
        self.path = StringVar(master)

    def run(self, kstart=None):
        urll = self.bvm.run(e_url.get(), e_url.get()[:2])  # av91882697 av  BV1bC4y1H7FJ
        tit = self.bvm.gettitle(urll[0])
        self.bd.run(dic=(self.path.get() + '/' + tit), urll=urll, kstart=kstart)  # ./title

    def selectPath(self):
        targetpath = askdirectory()
        self.path.set(targetpath)


if __name__ == '__main__':
    # Tkinter图形界面
    root = Tk()
    root.title('哔哩哔哩一键下载器')
    m = Manager(root)

    l_url = Label(root, text='视频编号', font="方正舒体")
    l_url.grid(row=0, sticky=W)

    e_url = Entry(root)
    e_url.grid(row=0, column=1, sticky=E)

    # 第二行,目标路径标签及路径选择按钮
    l_path = Label(root, text="目标路径:", font="方正舒体")
    l_path.grid(row=1, column=0)

    e_path = Entry(root, textvariable=m.path)
    e_path.grid(row=1, column=1)

    selectkey = Button(root, text="路径选择", command=m.selectPath, font="方正舒体")
    selectkey.grid(row=1, column=2)

    # 第三行登陆按扭，command绑定事件,激发下载事件

    downkey = Button(root, text='下载', command=m.run, font="方正舒体")
    downkey.grid(row=2, column=0, sticky=E)

    quitkey = Button(root, text="退出", command=root.quit, font="方正舒体")
    quitkey.grid(row=2, column=1, sticky=E)

    root.mainloop()
