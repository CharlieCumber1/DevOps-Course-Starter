import pytest
import requests
from dotenv import load_dotenv, find_dotenv
import app
import trello_items as trello

class MockResponse:
    def __init__(self, url):
        self.url = url
        self.list_info = [
                {"id": "mock_list_id_not_started", "name": "Not Started"},
                {"id": "mock_list_id_in_progress", "name": "In Progress"},
                {"id": "mock_list_id_done", "name": "Done"}
            ]
        self.not_started_list = [
                {
                    "id": "5f2d2a02e5623c443d7d5190",
                    "dateLastActivity": "2020-08-07T10:16:34.157Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_not_started",
                    "name": "Item 1"
                },
                {
                    "id": "5f2d2a051fe01a43d4a3dc0b",
                    "dateLastActivity": "2020-08-07T10:16:37.040Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_not_started",
                    "name": "Item 2"
                },
                {
                    "id": "5f2d2a0893cdbf6a1d4020bb",
                    "dateLastActivity": "2020-08-07T10:16:40.598Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_not_started",
                    "name": "Item 3"
                },
                {
                    "id": "5f2d2a0d42022d54874e390b",
                    "dateLastActivity": "2020-08-07T10:16:45.924Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_not_started",
                    "name": "Item 4"
                }
            ]
        self.in_progress_list = [
                {
                    "id": "5f2d2a2b4ad6605817a8ad7c",
                    "dateLastActivity": "2020-08-07T10:17:15.007Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_in_progress",
                    "name": "Item 5"
                },
                {
                    "id": "5f2d2a2e73b9781a72557d06",
                    "dateLastActivity": "2020-08-07T10:17:18.761Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_in_progress",
                    "name": "Item 6"
                },
                {
                    "id": "5f2d2a32a2a49e5639fe6eb6",
                    "dateLastActivity": "2020-08-07T10:17:22.185Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_in_progress",
                    "name": "Item 7"
                },
                {
                    "id": "5f2d2a388dce853c3ca9f756",
                    "dateLastActivity": "2020-08-07T10:17:28.190Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_in_progress",
                    "name": "Item 8"
                }
            ]
        self.done_list = [
                {
                    "id": "5f2d2a3ccea4473780f1adea",
                    "dateLastActivity": "2020-08-07T10:17:32.700Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_done",
                    "name": "Item 9"
                },
                {
                    "id": "5f2d2a3f65144029b6205d3e",
                    "dateLastActivity": "2020-08-07T10:17:35.419Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_done",
                    "name": "Item 10"
                },
                {
                    "id": "5f2d2a42bc6c370f65f74d64",
                    "dateLastActivity": "2020-08-07T10:17:38.105Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_done",
                    "name": "Item 11"
                },
                {
                    "id": "5f2d2a450e99c347e8458c7b",
                    "dateLastActivity": "2020-08-07T10:17:41.311Z",
                    "desc": "",
                    "idBoard": "mock_board_id",
                    "idList": "mock_list_id_done",
                    "name": "Item 12"
                }
            ]

    def json(self):
        if self.url == 'https://api.trello.com/1/boards/mock_board_id/lists':
            return self.list_info
    
        if self.url == 'https://api.trello.com/1/lists/mock_list_id_not_started/cards':
            return self.not_started_list
        
        if self.url == 'https://api.trello.com/1/lists/mock_list_id_in_progress/cards':
            return self.in_progress_list

        if self.url == 'https://api.trello.com/1/lists/mock_list_id_done/cards':
            return self.done_list


@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    def mock_get(url, **kwargs):
        return MockResponse(url)

    monkeypatch.setattr(requests, 'get', mock_get)
    response = client.get('/')

    assert 'Item 4' in response.data.decode()
    assert 'Item 5' in response.data.decode()
    assert 'Item 8' in response.data.decode()
    assert 'Item 9' in response.data.decode()
    assert 'Item 12' in response.data.decode()

def test_mock_list_info_response(monkeypatch, client):
    def mock_get(url, **kwargs):
        return MockResponse(url)

    monkeypatch.setattr(requests, 'get', mock_get)

    not_started_list_info = trello.get_list_info('Not Started')
    in_progress_list_info = trello.get_list_info('In Progress')
    done_list_info = trello.get_list_info('Done')

    assert not_started_list_info['id'] == 'mock_list_id_not_started'
    assert in_progress_list_info['id'] == 'mock_list_id_in_progress'
    assert done_list_info['id'] == 'mock_list_id_done'

def test_mock_get_all_items(monkeypatch, client):
    def mock_get(url, **kwargs):
        return MockResponse(url)

    monkeypatch.setattr(requests, 'get', mock_get)

    assert trello.get_item('5f2d2a051fe01a43d4a3dc0b').title == 'Item 2'
    assert trello.get_item('5f2d2a32a2a49e5639fe6eb6').title == 'Item 7'
    assert trello.get_item('5f2d2a3ccea4473780f1adea').title == 'Item 9'
    assert trello.get_item('5f2d2a450e99c347e8458c7b').title == 'Item 12'