from datetime import datetime
from tech_news.database import find_news, search_news


# Requisito 6
def search_by_title(title):
    news_from_db = find_news()
    page = []

    for news in news_from_db:
        if title.lower() in news["title"].lower():
            page.append((news["title"], news["url"]))
    return page


# method lower https://www.w3schools.com/python/ref_string_lower.asp;


# Requisito 7
def search_by_date(date):
    try:
        date_imputed = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        date_from_db = {"timestamp": date_imputed}
        news_search = search_news(date_from_db)
        if news_search:
            return [(news["title"], news["url"]) for news in news_search]
        else:
            return []
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    new_search = search_news(
        {"tags": {"$elemMatch": {"$regex": tag, "$options": "i"}}}
    )
    return [(news["title"], news["url"]) for news in new_search]


# Requisito 9
def search_by_category(category):
    new_search = search_news({"category": category})
    return [(news["title"], news["url"]) for news in new_search]