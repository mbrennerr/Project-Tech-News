from tech_news.database import get_collection


# Requisito 10
class Utils:
    @staticmethod
    def get_by_title_and_url(news: list) -> list:
        def transform_news(item: dict) -> dict:
            return (
                item["title"],
                item["url"],
            )

        transformed_news = map(transform_news, news)
        return list(transformed_news)

    def single_categories(result: list) -> list:
        def transform_item(item: dict) -> dict:
            return item["_id"]

        transformed_result = map(transform_item, result)
        return list(transformed_result)


def top_5_news():
    new_search = list(
        get_collection()
        .find()
        .sort([("comments_count", -1), ("title", 1)])
        .limit(5)
    )

    return Utils.get_by_title_and_url(new_search)


# Requisito 11


def top_5_categories():
    new_search = list(
        get_collection().aggregate(
            [
                {"$group": {"_id": "$category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1, "_id": 1}},
            ]
        )
    )

    return Utils.single_categories(new_search)
