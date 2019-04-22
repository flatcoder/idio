from flask_script import Command, Option
from flask import jsonify
from app.config import site_rules
from app.models import UrlIndex
from bs4 import BeautifulSoup
import requests
import json

class idioParser:
    headers = {"Accept-Language": "en-GB, en;q=0.5"}
    timeout = 5

    def parse(self,url,is_sitemap=False):
        if not is_sitemap:
            return self._parse(url)

        # else, it's a site map
        try:
            page = requests.get(url,headers=self.headers,timeout=self.timeout)
        except:
            # connection error
            return None, None, None

        soup = BeautifulSoup(page.text, 'lxml')
        urls = soup.find_all('loc')
        for url in urls:
            title, content, images = self._parse(url.text)

        # return results for the LAST url crawled
        return title, content, images

    def _parse(self,url):
        target_site = None
        update_mode = False
        for domain in site_rules:
            if domain in url:
                target_site = site_rules[domain]
                break

        if target_site == None:
            raise Exception("Target site is unsupported.")


        # check if we have the URL already and are allowed to upsert
        if UrlIndex.find(url=url) != None:
            if target_site["update_existing"]:
                print("UPDATE EXISTING: "+url)
                update_mode = True
            else:
                print("SKIP DUPE: "+url)
                return None,None,None
            # print("It's an update!")

        # category if applicable
        category = ""
        if target_site["category_uri"] != None:
            if int(target_site["category_uri"]) >= 0:
                bits =  url.split('/')
                try:
                    category = bits[target_site["category_uri"]]
                except:
                    # non-standard URI, category unknown
                    category = ""

        for il in target_site["ignore_list"]:
            if il in url:
                print("SKIPPING: "+url)
                return None,None,None
        print("CRAWLING: "+url)

        try:
            page = requests.get(url, headers=self.headers,timeout=self.timeout)
        except:
            # connection error
            return None, None, None

        soup = BeautifulSoup(page.text, 'html.parser')
        title = self._get_title(target_site, soup)
        content = self._get_content(target_site, soup)
        images = list()

        if target_site["image_wrap"] != "" and target_site["image_wrap"] != None:
            pics_wrapped = soup.find_all(target_site["image_wrap"])#, class_='picture')
        else:
            pics_wrapped = soup.find_all('body')#, class_='picture')

        for wrap in pics_wrapped:
            ims = wrap.find_all(target_site["image_tag"])
            for im in ims:
                try:
                    if im["alt"] != "" or target_site["must_have_alt"] == False:
                        images.append( { "src": im["src"].split('?')[0], "alt": im["alt"] })
                except:
                    if target_site["must_have_alt"] == False:
                        images.append( { "src": im["src"].split('?')[0], "alt": "aa" })

        canonicals = soup.find_all("link", rel="canonical")
        #print(canonicals)
        if canonicals == None or canonicals == "":
            canonical = url
        else:
            for link in canonicals:
                if str(link) != "":
                    canonical = link['href']
                    break

        ims = json.dumps(images)
        if update_mode:
            UrlIndex.update(url, title, content, canonical, images=ims, category=category)
        else:
            UrlIndex.create(url, title, content, canonical, images=ims, category=category)

        return title, content, images

    def _get_title(self, target_site, soup):
        try:
            title = soup.find(class_= target_site['title']).text
            return title.strip()
        except:
            return ""

    def _get_content(self, target_site, soup):
        try:
            content = ""
            for content_area in target_site['content']:
                #print(content_area)
                cn = soup.find(class_= content_area).find_all(target_site['content_tag'])
                for c in cn:
                    if c != None:
                        content = content + c.text.strip() +"\n"#soup.find(class_= content_area).text
            return content.strip()
        except:
            return ""

class ScrapeCommand(Command):
    "Idio Scraper"

    option_list = (
        Option('--sitemap', '-s', dest='sitemap'),
        Option('--url', '-u', dest='url'),
    )

    def run(self, sitemap, url):
        if sitemap == None and url == None:
            print("Specify a sitemap or single URL. Use -? for help.")
            return False

        if sitemap != None and url != None:
            print("Specify a sitemap -OR- single URL, not both. Use -? for help.")
            return False

        parser = idioParser()
        if sitemap != None:
            # we'll get the last entry crawled as a result
            last_title, last_content, last_images = parser.parse(sitemap,is_sitemap=True)
        else:
            # only one result
            title, content, images = parser.parse(url,is_sitemap=False)
