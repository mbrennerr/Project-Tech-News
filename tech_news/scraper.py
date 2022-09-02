import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    time.sleep(1)
    fake_headers = ({"user-agent": "Fake user-agent"},)
    try:
        res = requests.get(url, headers=fake_headers, timeout=3)
        res.raise_for_status()
    except (requests.HTTPError, requests.Timeout):
        return None
    return res.text


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(html_content)
    notice_list = []
    tag_content = "h2.entry-title a ::attr(href)"
    for quot in selector.css(tag_content):
        notice_list.append(quot.get())

    return notice_list


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(html_content)
    tag_content = "a.next::attr(href)"
    call_next = selector.css(tag_content).get()
    return call_next


# Requisito 4
def scrape_noticia(html_content):
    selector = Selector(text=html_content)
    url = selector.css("link[rel='canonical']::attr(href)").get().strip()
    title = selector.css("h1.entry-title::text").get().strip()
    time_stamp = selector.css(".meta-date::text").get().strip()
    writer = selector.css(".author a::text").get()
    comments = len(selector.css(".comment-list li").getall())
    summary = "".join(
        selector.css(".entry-content > p:first-of-type *::text").getall()
    ).strip()
    tags_content = selector.css(".post-tags a::text").getall()
    category = selector.css(".label::text").get().strip()

    return {
        "url": url,
        "title": title,
        "timestamp": time_stamp,
        "writer": writer,
        "comments_count": comments,
        "summary": summary,
        "tags": tags_content,
        "category": category,
    }


# Requisito 5
def get_tech_news(amount):
    list_of_news = []
    url = "https://blog.betrybe.com/"
    fetch_html = fetch(url)

    while True:
        news_list = scrape_novidades(fetch_html)

        for news in news_list:
            news_html = fetch(news)
            scrapped_news = scrape_noticia(news_html)
            list_of_news.append(scrapped_news)

            if len(list_of_news) == amount:
                create_news(list_of_news)
                return list_of_news

        next_page = scrape_next_page_link(fetch_html)
        fetch_html = fetch(next_page)
