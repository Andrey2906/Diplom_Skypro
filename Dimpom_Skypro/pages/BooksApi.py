import pytest
import requests
from typing import Dict, Any
from config.api_config import BASE_URL_V1, BASE_URL_V2, list_books_params


class BooksApi:

    def __init__(self, session) -> None:
        self.session = session

    def get_list_books(self) -> requests.Response:
        """
        Этот метод возвращает JSON с книгами
        """
        response = self.session.get(BASE_URL_V2, params=list_books_params)
        return response

    def books_canBuy(self, data) -> Dict[str, Any]:
        """
        Этот метод возвращает нам первую книгу из списка доступную к покупке
        """
        book = next(
            (b for b in data["data"] if b["attributes"]
             ["status"] == "canBuy"), None)
        if book is None:
            pytest.skip("Нет доступных книг для покупки")
        return book

    def get_id(self, slug_id) -> requests.Response:
        """
        Этот метод запрашивает данные книги по конкретному ID
        """
        get_by_id = self.session.get(f"{BASE_URL_V1}products/slug/{slug_id}")
        return get_by_id

    def add_bookmark(
            self, book_id) -> requests.Response:
        """
        Этот метод добавляет книгу в раздел Закладок по заданному ID
        """
        bookmark = self.session.post(
            f"{BASE_URL_V1}bookmarks", json={"id": book_id})
        return bookmark

    def delete_bookmark(self, book_id) -> requests.Response:
        """
        Этот метод удаляет книгу из раздела Закладок по заданному ID
        """
        bookmark = self.session.delete(
            f"{BASE_URL_V1}bookmarks", json={"id": book_id})
        return bookmark
