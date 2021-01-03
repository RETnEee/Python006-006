import requests
from lxml import etree
from queue import Queue
import threading
import json
from pathlib import *
import re

class CrawThread(threading.Thread):
    def __init__(self, thread_id, queue):
        super().__init__()
        self.thread_id = thread_id
        self.queue = queue
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
            "Referer": "https://www.zhihu.com/question/24863332",
        }
    
    def run(self):
        print(f"启动线程：{self.thread_id}")
        self.scheduler()
        print(f"结束线程：{self.thread_id}")

    def scheduler(self):
        while not self.queue.empty():
            page = self.queue.get()
                    #请求参数
            limit = 15
            offset = 0
            params = {
                "limit":limit,
                "offset":offset, 
                "sort_by":"sort_by", 
                "platform":"desktop",
                "include":"data[*].is_normal,content"}
            question_id = "24863332"
            url = f"https://www.zhihu.com/api/v4/questions/{question_id}/answers"

            try:
                response = requests.get(url, headers = self.headers, params=params)
                dataQueue.put(response.text)
            except Exception as e:
                print("下载异常", e)

class ParseThread(threading.Thread):
    def __init__(self, thread_id, queue, file):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.queue = queue
        self.file = file

    def run(self):
        print(f"开始线程:{self.thread_id}")
        while flag:
            try:
                item = self.queue.get(False)
                if not item:
                    continue
                self.parse_data(item)
                self.queue.task_done()
            except Exception as e:
                pass
        print(f"结束线程：{self.thread_id}")

    def parse_data(self, item):
        try:
            res = json.loads(item)
            datas = res['data']
            title = datas[0]['question']['title']
            comment = f"内容\n\n\n"
            if datas is not None:
                for data in datas:
                    author = data["author"]["name"]
                    comment += f"author: {author}\n"
                    content = data["content"]
                    res_tr = r'<p>(.*?)</p>'
                    m_tr =  re.findall(res_tr,content,re.S|re.M)
                    for s in m_tr:
                        comment += f"{s}\n"
                    if not m_tr:
                        comment += f"{content}\n\n"
            path = Path(__file__)
            parent_path = path.resolve().parent
            file_path = parent_path.joinpath(f"zhihu-{title}.txt")
            with open(file_path, 'w') as fp:
                if title:
                    fp.writelines(title)
                if comment:
                    fp.writelines(comment)
        except Exception as e2:
            print(f"error parse", e2)

if __name__ == "__main__":
    pageQueue = Queue(1)
    for page in range(0, 1):
        pageQueue.put(page)

    dataQueue = Queue()

    crawl_threads = []
    crawl_name_list = ["crawl_1", "crawl_2", "crawl_3"]
    for thread_id in crawl_name_list:
        thread = CrawThread(thread_id, pageQueue)
        thread.start()
        crawl_threads.append(thread)

    with open("book.json", "a", encoding="utf-8") as pipeline_f:
        parse_thread = []
        parse_name_list = ["parse_1", "parse_2", "parse_3"]
        flag = True
        for thread_id in parse_name_list:
            thread = ParseThread(thread_id, dataQueue, pipeline_f)
            thread.start()
            parse_thread.append(thread)

        for t in crawl_threads:
            t.join()

        flag = False
        for t in parse_thread:
            t.join()

    print("exit")

    

