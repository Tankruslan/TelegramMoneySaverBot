from typing import Dict, List, NamedTuple

import db


class Category(NamedTuple):
    """ Structure of category """
    name: str
    is_primary_expense: bool
    aliases: List[str]


class Categories:
    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """ Get categories from DB """
        categories = db.fetchall(
            "category", "name is_primary_expense aliases".split()
        )
        categories = self._fill_aliases(categories)
        return categories

    @staticmethod
    def _fill_aliases(categories: List[Dict]) -> List[Category]:
        """ Fill categories with its aliases """
        filled_categories = []
        for index, category in enumerate(categories):
            aliases = [alias for alias in category["aliases"].split(",") if alias]
            aliases = [alias.strip() for alias in aliases]
            aliases.append(category["name"])
            filled_categories.append(
                Category(
                    name=category['name'],
                    is_primary_expense=category['is_primary_expense'],
                    aliases=aliases
                )
            )
        return filled_categories

    def get_all_categories(self) -> List[Category]:
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """ Get category by its alias """
        found = None
        other_category = None
        for category in self._categories:
            if category.name == "other":
                other_category = category
            for alias in category.aliases:
                if category_name in alias:
                    found = category
        if not found:
            found = other_category
        return found
