import io
import math
import os
import re
import sqlite3
from zipfile import ZipFile

from PIL import Image
from dotenv import load_dotenv
from flask import Flask, jsonify, request, make_response, send_from_directory
from flask_cors import CORS

load_dotenv()

file_settings = os.getenv('DATABASE')  # 'Guerra Civil'

default_folder = os.getenv('DEFAULTFOLDER') + file_settings  # "A:\\Arquivos SSD\\Mangas\\" + file_settings


def get_cursor():
    con = sqlite3.connect(file_settings + '.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return cur


app = Flask(__name__, static_url_path='', static_folder=os.getenv('STATICFOLDER'))

CORS(app, resources={r'/*': {'origins': '*'}})


def get_book_info(cur, galleryId):
    cur.execute("select * from Gallery where id = ?;", (galleryId,))
    book_info = dict(cur.fetchone())
    if book_info is None:
        raise Exception
    book_info['tags'] = re.sub(r'\' | \'|\[|]|\'', '', book_info['tags']).split(',')
    return book_info


def get_input_zip(book_info):
    message = None
    try:
        for filename in os.listdir(default_folder + "\\" + book_info['artist']):
            # print("[" + book_info['artist'] + '] ' + book_info['title'])
            if filename.startswith("[" + book_info['artist'] + '] ' + book_info['title'] + ' ('):
                message = os.path.join(book_info['artist'], filename)
    except FileNotFoundError as error:
        print(error)
    if message is None:
        for filename in os.listdir(default_folder + "\\Books"):
            if filename.startswith(str(book_info['id']) + ' '):
                message = os.path.join("Books", filename)
    input_zip = default_folder + "\\" + message
    return ZipFile(input_zip)


@app.route('/api/view/<int:galleryId>')
def request_book_info(galleryId):
    cur = get_cursor()
    book_info = get_book_info(cur, galleryId)
    input_zip = get_input_zip(book_info)
    namelist = input_zip.namelist()
    response_object = {'book_info': book_info, 'pages': namelist}
    return jsonify(response_object)


def resize_image(image_binary, width=480, height=672):
    image = Image.open(io.BytesIO(image_binary))
    resized_image = image.resize((width, height))
    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='png')
    return img_byte_arr.getvalue()


@app.route('/api/cover/<int:galleryId>')
def get_cover(galleryId):
    resize = request.args.get('resize')
    cur = get_cursor()
    book_info = get_book_info(cur, galleryId)
    input_zip = get_input_zip(book_info)
    namelist = input_zip.namelist()
    if resize != 'False':
        response = make_response(resize_image(input_zip.read(namelist[0])))
    else:
        response = make_response(input_zip.read(namelist[0]))
    response.headers.set('Content-Type', 'image/png')
    return response


@app.route('/api/view/page/thumb/<int:galleryId>/<pageName>')
def get_page_thumb(galleryId, pageName):
    cur = get_cursor()
    book_info = get_book_info(cur, galleryId)
    input_zip = get_input_zip(book_info)
    response = make_response(resize_image(input_zip.read(pageName)))
    response.headers.set('Content-Type', 'image/png')
    return response


@app.route('/api/view/page/<int:galleryId>/<pageName>')
def get_page(galleryId, pageName):
    cur = get_cursor()
    book_info = get_book_info(cur, galleryId)
    input_zip = get_input_zip(book_info)
    if pageName != 'all-pages':
        image_binary = input_zip.read(pageName)
    else:
        namelist = input_zip.namelist()
        image_binary = input_zip.read(namelist[0])
    response = make_response(image_binary)
    response.headers.set('Content-Type', 'image/jpeg')
    return response


def prepare_statements(query, tag, artist, book,
                       circle,
                       event,
                       language,
                       magazine,
                       parody,
                       publisher, offset, limit):
    sql = "SELECT id as bookid, artist, description, extension , subcategory, tags," \
          " title, title_conventional, 'type' FROM Gallery"
    sql2 = ""
    fields = list()
    fields.append(offset)
    fields.insert(0, limit)
    position = 0

    if query is not None:
        fields.insert(position, '%' + query + '%')
        position = position + 1
        fields.insert(position, '%' + query + '%')
        position = position + 1
        fields.insert(position, '%' + query + '%')
        position = position + 1
        sql2 = " where (artist like ? or title like ? or tags like ?)"
    if artist is not None:
        fields.insert(position, '%' + artist + '%')
        sql2 = " where artist like ?" if sql2 == "" else sql2 + " and artist like ?"
        position = position + 1

    if tag is not None:
        fields.insert(position, '%' + tag + '%')
        sql2 = ' where tags like ? ' if sql2 == "" else sql2 + " and tags like ?"
        position = position + 1

    if book is not None:
        fields.insert(position, book)
        sql2 = ' where book = ? ' if sql2 == "" else sql2 + " and book = ?"
        position = position + 1

    if circle is not None:
        fields.insert(position, circle)
        sql2 = ' where circle = ? ' if sql2 == "" else sql2 + " and circle = ?"
        position = position + 1

    if event is not None:
        fields.insert(position, event)
        sql2 = ' where event = ? ' if sql2 == "" else sql2 + " and event = ?"
        position = position + 1

    if language is not None:
        fields.insert(position, language)
        sql2 = ' where language = ? ' if sql2 == "" else sql2 + " and language = ?"
        position = position + 1

    if magazine is not None:
        fields.insert(position, magazine)
        sql2 = ' where magazine = ? ' if sql2 == "" else sql2 + " and magazine = ?"
        position = position + 1

    if parody is not None:
        fields.insert(position, parody)
        sql2 = ' where parody = ? ' if sql2 == "" else sql2 + " and parody = ?"
        position = position + 1

    if publisher is not None:
        fields.insert(position, publisher)
        sql2 = ' where publisher = ? ' if sql2 == "" else sql2 + " and publisher = ?"

    fields = tuple(fields)
    sql = sql + sql2 + " order by id asc limit ? offset ? ;"
    return sql, fields, sql2


@app.route('/api/books')
def get_books():
    offset = request.args.get('page')
    limit = request.args.get('limit')
    tag = request.args.get('tag')
    book = request.args.get('book')
    circle = request.args.get('circle')
    event = request.args.get('event')
    language = request.args.get('language')
    magazine = request.args.get('magazine')
    parody = request.args.get('parody')
    publisher = request.args.get('publisher')
    artist = request.args.get('artist')
    query = request.args.get('query')
    if limit is None:
        limit = 30
    if offset is None or offset == 1:
        offset = 0
    else:
        offset = (int(offset) * limit) - limit
    cur = get_cursor()
    response_object = {}
    sql, fields, sql2 = prepare_statements(query=query, tag=tag, artist=artist, offset=offset, book=book, circle=circle,
                                           event=event, language=language, magazine=magazine, parody=parody,
                                           publisher=publisher, limit=limit)

    cur.execute(sql, fields)
    data = [dict(row) for row in cur.fetchall()]
    response_object['books'] = data
    fullsql = "select count(*) from Gallery" + sql2 + " limit ? + 1 + ?;"
    # print(fullsql, fields)
    cur.execute(fullsql, fields)
    pages = cur.fetchone()
    response_object['pages'] = math.ceil(pages[0] / 30)
    cur.close()
    return jsonify(response_object)


@app.route('/api/artists')
def get_artists():  # put application's code here
    cur = get_cursor()
    cur.execute("select artist from Gallery group by artist order by artist;", ())
    data = [row[0] for row in cur.fetchall()]
    # print(data)
    response_object = {'artists': data}
    return jsonify(response_object)


@app.route("/css/<string:path>")
def get_css(path):  # put application's code here
    return send_from_directory(app.static_folder + '\\css', path)


@app.route("/js/<string:path>")
def get_js(path):  # put application's code here
    return send_from_directory(app.static_folder + '\\js', path)


@app.route('/', defaults={'path': '', 'path2': '', 'path3': ''})
@app.route("/<string:path>")
@app.route('/<path:path>')
@app.route("/<string:path>/<string:path2>")
@app.route('/<path:path>/<path:path2>')
@app.route("/<string:path>/<string:path2>/<string:path3>")
@app.route('/<path:path>/<path:path2>/<path:path3>')
def hello_world(path=0, path2=0, path3=0):  # put application's code here
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(port=8080, host="0.0.0.0")
