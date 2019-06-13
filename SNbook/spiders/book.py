# -*- coding: utf-8 -*-
import scrapy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com/']

    def parse(self, response):
        doc1_list = response.xpath("//div[@class='menu-list']/div[@class='menu-item']")
        for i, doc1 in enumerate(doc1_list):
            item = {}
            item["doc1_name"] = doc1.xpath(".//h3/a/text()").extract_first()
            # print(doc1_name)
            item["doc1_href"] = doc1.xpath(".//h3/a/@href").extract_first()
            # print(doc1_href)
            # 找当前根目录下的对应的那一个分级目录
            to_doc2 = response.xpath("//div[@class='menu-list']//div[contains(@class,'menu-sub')][{}]/div[@class='submenu-left']".format(i+1))
            # print(to_doc2)
            doc2_list = to_doc2.xpath(".//p")
            for l, doc2 in enumerate(doc2_list):
                item["doc2_name"] = doc2.xpath("./a/text()").extract_first()
                # print(doc2_name)
                item["doc2_href"] = doc2.xpath("./a/@href").extract_first()
                # print(doc2_href)
                # // div[@class ='menu-list'] //div[contains(@class ,'menu-sub')][1]//ul/li
                to_doc3 = response.xpath("//div[@class ='menu-list']//div[contains(@class ,'menu-sub')][{}]/div[@class='submenu-left']".format(l+1))
                doc3_list = to_doc3.xpath(".//ul/li")
                for doc3 in doc3_list:
                    item["doc3_name"] = doc3.xpath("./a/text()").extract_first()
                    # print(doc3_name)
                    item["doc3_href"] = doc3.xpath("./a/@href").extract_first()
                    # print(doc3_href)
                    # print(item)
                    # 发送请求
                    yield scrapy.Request(
                        item["doc3_href"],
                        callback=self.parse_detail,
                        meta={"wmp": item}
                    )


    def parse_detail(self, response):
        with open("./book.html", "w", encoding="utf-8") as f:
            f.write(response.body.decode())


        item = response.meta["wmp"]
        item["book_content"] = response.xpath("//li[contains(@class ,'product')]//img/@alt").extract()
        item["book_img"] = response.xpath("//li[contains(@class ,'product')]//div[@class='img-block']/a/img/@src2").extract_first() #TODO
        # item["book_img"] = ["https:" + i for i in item["book_img"]] 错误
        item["book_img"] = "https:" + item["book_img"]
        # print(item["book_img"])
        item["book_addr"] =response.xpath("//li[contains(@class ,'product')]//p[@class='seller oh no-more ']/a/text()").extract_first()
        # print(item["book_addr"])
        # print(item)
        # logger.warning(item)
        yield item