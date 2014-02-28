import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
render_template
import os
import Quote

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'mapper.db'),
	DEBUG=True,
	SECRET_KEY='devkey',
	USERNAME='admin',
	PASSWORD='password'
	))
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.before_request
def before_request():
    get_db()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'db'):
        g.db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def display_all():
    all_quotes = []
    quote_ids = g.db.execute('select id from quotes;').fetchall()
    quote_ids = [int(i[0]) for i in quote_ids]
    for i in quote_ids:
        quote_query = g.db.execute('select * from quotes where id = ?;',[i]).fetchone()
        tags = g.db.execute('select tag from tags where quote_id = ?;',[i]).fetchall()
        tags_for_post = []
        for tag in tags:
            tags_for_post.append(tag[0])
        current_quote = Quote.Quote(quote_query[0],quote_query[1],quote_query[2],quote_query[3],quote_query[4],tags_for_post)
        all_quotes.append(current_quote)
    return render_template('quotes.html', quotes = all_quotes)
@app.route('/tag/<tag>')
def display_tag(tag):
    tagged_quotes = []
    quote_ids = g.db.execute('select q.id from quotes as q, tags as t where q.id = t.quote_id and t.tag = ?;',[tag]).fetchall()
    quote_ids = [int(i[0]) for i in quote_ids]
    for i in quote_ids:
        quote_query = g.db.execute('select * from quotes where id = ?;',[i]).fetchone()
        tags = g.db.execute('select tag from tags where quote_id = ?;',[i]).fetchall()
        tags_for_post = []
        for tag in tags:
            tags_for_post.append(tag[0])
        current_quote = Quote.Quote(quote_query[0],quote_query[1],quote_query[2],tags_for_post)
        tagged_quotes.append(current_quote)
    return render_template('quotes.html', quotes = tagged_quotes)

@app.route('/insert',methods=['GET','POST'])
def insert():
    if request.method == 'POST':
        q_title = request.form['q_title']
        q_quote = request.form['q_quote']
        q_isbn = request.form['q_isbn']
        q_page_no = request.form['q_page_no']
        q_tags = request.form['q_tags'].split(', ')
        g.db.execute('insert into quotes values (NULL, ?, ?, ?, ?)', [q_title, q_quote, q_isbn, q_page_no])
        g.db.commit()
        new_id = int(g.db.execute('select id from quotes order by id desc limit 1;').fetchone()[0])
        for tag in q_tags:
            g.db.execute('insert into tags values (?, ?);',[new_id,tag])
        g.db.commit()
    return render_template('insert.html')
@app.route('/delete/<id>')
def delete(id):
    g.db.execute('delete from quotes where id = ?', [id])
    g.db.execute('delete from tags where quote_id = ?',[id])
    g.db.commit()
    return redirect('/')


@app.route('/reset')
def reset():
    init_db()
    return redirect(url_for('display_all'))





if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080)
    