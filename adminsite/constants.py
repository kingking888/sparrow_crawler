class CrawlStatus(object):
    # 爬取完毕
    DONE = "done"
    # 还没有爬取
    TODO = 'todo'
    # 正在进行
    GOING = 'going'

class TaskType(object):
    # 爬取任务
    CRAWL="crawl"
    # EXCEL导入
    EIMPORT="eimport"
    # EXCEL导出
    EEXPORT="eexport"