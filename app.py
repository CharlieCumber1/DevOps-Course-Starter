from flask import Flask, render_template, request, redirect, url_for
from operator import itemgetter 
import trello_items as trello

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index(): 
    if request.method == 'POST':
        trello.add_item(request.form.get('title'), request.form.get('description'))
    return render_template('/index.html', all_items=trello.get_items())

@app.route('/toggle-completion/<id>')
def toggle(id):
    trello.toggle_status(id)
    return redirect('/')

@app.route('/delete/<id>')
def delete_item(id):
    trello.delete_item(id)
    return redirect('/')

if __name__ == '__main__':
    app.run()
