import os
from task_item import Item
import requests
import json

def get_auth_params():
    trello_key = os.environ.get('TRELLO_KEY')
    trello_token = os.environ.get('TRELLO_TOKEN')
    return { 'key': trello_key, 'token': trello_token }

def build_url(endpoint):
    return 'https://api.trello.com/1' + endpoint

def build_params(params = {}):
    full_params = get_auth_params()
    full_params.update(params)
    return full_params

def get_lists_info():
    params = build_params({ 'cards': 'open' })
    board_id = os.environ.get('TRELLO_BOARD')
    url = build_url(f'/boards/{board_id}/lists')
    response = requests.get(url, params=params)
    lists = response.json()
    return lists

def get_list_info(name):
    lists = get_lists_info()
    return next((list for list in lists if list['name'] == name), None)

def get_list_id(name):
    list_info = get_list_info(name)
    return list_info['id']


def get_items():
    lists = get_lists_info()
    items = []

    for card_list in lists:
        params = build_params({ 'cards': 'open' })
        list_id = card_list['id']
        url = build_url(f'/lists/{list_id}/cards')

        response = requests.get(url, params=params)
        cards = response.json()
        for card in cards:
            items.append(Item.from_trello_card(card, card_list['name']))

    return items

def get_item(id):
    items = get_items()
    return next((item for item in items if item.id == id), None)

def add_item(title, description):
    list_id = get_list_id('Not Started')
    params = build_params({ 'name': title, 'idList': list_id })
    url = build_url('/cards')
    requests.post(url, params=params)
    return title

def set_status_not_started(id):
    item = get_item(id)
    item.set_status_not_started()
    save_item(item)
    return

def set_status_in_progress(id):
    item = get_item(id)
    item.set_status_in_progress()
    save_item(item)
    return

def set_status_completed(id):
    item = get_item(id)
    item.set_status_completed()
    save_item(item)
    return

def save_item(item):
    list_id = get_list_id(item.status)
    params = build_params({ 'name': item.title, 'dec': item.description, 'idList': list_id})
    url = build_url(f'/cards/{item.id}')
    requests.put(url, params=params)
    return

def delete_item(id):
    params = build_params()
    url = build_url(f'/cards/{id}')
    requests.delete(url, params=params)  
    return

def create_board(name):
    params = build_params({ 'name': name })
    url = build_url('/boards/')
    response = requests.post(url, params=params)
    board = response.json()
    board_id = board['id']

    create_list('Not Started', board_id)
    create_list('In Progress', board_id)
    create_list('Done', board_id)

    return board_id

def delete_board(id):
    params = build_params()
    url = build_url(f'/boards/{id}')
    requests.delete(url, params=params)
    return

def create_list(name, board_id):
    params = build_params({ 'name': name, 'idBoard': board_id })
    url = build_url('/lists')

    requests.post(url, params=params)
    return