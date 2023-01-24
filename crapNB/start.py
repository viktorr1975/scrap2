from scrapy import cmdline
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
#from crapNB.spiders import firstspider
import subprocess
import time

if __name__ == '__main__':
#    sys.path.append('/home/vit/PycharmProjects/scrap2/crapNB')     # appending a path to scrapy project
#    print(sys.path)
    start_time = time.time()
#scrapy crawl itcast (notebooks is the crawler name)
    #cmdline.execute("scrapy crawl ctlnk".split())
    #cmdline.execute("scrapy crawl holod".split())

    # subprocess.run("scrapy crawl ctlnk --nolog".split())
    # subprocess.run("scrapy crawl holod --nolog".split())
    subprocess.run("python3 -m scrapy crawl holod --nolog", shell=True, env={**os.environ, 'PYTHONPATH': ';'.join(sys.path)})
    subprocess.run("python3 -m scrapy crawl ctlnk --nolog", shell=True, env={**os.environ, 'PYTHONPATH': ';'.join(sys.path)})


    # process = CrawlerProcess(get_project_settings())
    # # 'holod' is the name of one of the spiders of the project.
    # process.crawl('holod')
    # process.start() # the script will block here until the crawling is finished

    # process = CrawlerProcess(settings={
    #     "FEEDS": {
    #         "out.json": {"format": "json"},
    #     },
    # })
    # process.crawl(firstspider.ComputersSpider1) #паук для сайта https://www.citilink.ru/catalog/noutbuki
    # process.start()
    print("--- %s seconds ---" % (time.time() - start_time))