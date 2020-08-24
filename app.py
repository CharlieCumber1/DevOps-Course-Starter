from flask import Flask, render_template, request, redirect, url_for
import trello_items as trello
from view_model import ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.Config')
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            trello.add_item(request.form.get('title'), request.form.get('description'))
        items = trello.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/set-status/<id>/<status>')
    def set_status(id, status):
        if status == 'outstanding':
            trello.set_status_not_started(id)
        elif status == 'pending':
            trello.set_status_in_progress(id)
        elif status == 'completed':
            trello.set_status_completed(id)
        return redirect('/')

    @app.route('/delete/<id>')
    def delete_item(id):
        trello.delete_item(id)
        return redirect('/')
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run()