import requests
from trello_config import KEY, TOKEN, BOARD, PENDING, DONE
import json 

class Item:
    def __init__(self, card):
        self.id = card['id']
        self.title = card['name']
        if card['idList'] == PENDING:
            self.status = 'Not Started'
        elif card['idList'] == DONE:
            self.status = 'Completed'
        if card['desc'] != 'None':
            self.description = card['desc']

def get_items():
    response = requests.get(
        f'https://api.trello.com/1/boards/{BOARD}/cards',
        params={'key':KEY, 'token':TOKEN},
    )
    all_items = [Item(item) for item in response.json()]
    return all_items

def get_item(id):
    items = get_items()
    return next((item for item in items if item.id == id), None)

def add_item(title, description):
    requests.post(f'https://api.trello.com/1/cards?key={KEY}&token={TOKEN}&idList={PENDING}&name={title}&desc={description}')
    return title

def save_item(item):
    if item.status == 'Not Started':
        list_id = PENDING
    elif item.status == 'Completed':
        list_id = DONE
    requests.put('https://api.trello.com/1/cards/{id}?key={key}&token={token}&name={name}&idList={listId}'.format(id=item.id, key=KEY, token=TOKEN, name=item.title, listId=list_id))
    return

def toggle_status(id):
    item = get_item(id)
    if item.status == 'Not Started':
        item.status = 'Completed'
    elif item.status == 'Completed':
        item.status = 'Not Started'
    save_item(item)

def delete_item(id):
    requests.delete('https://api.trello.com/1/cards/{id}?key={key}&token={token}'.format(id=id, key=KEY, token=TOKEN))   
    return