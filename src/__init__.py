import io
import csv
import time
from flask import Flask, request, render_template, jsonify, send_file, g
from .database import Record, Database
from .llm import Model


app = Flask(__name__)
model = Model()
def get_db():
    if (db := getattr(g, 'db', None)) is None:
        db = g.db = Database()
    return db


@app.route('/', methods=['GET'])
def index():
    '''Render the main page of the web application.
    '''
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    '''Submit text for real-time analysis.
    '''
    request_body = request.get_json()
    labels, comment = [], ''
    if (text := request_body.get('text')):
        labels, comment = model(text)
        get_db().put(Record(
            created_at=int(time.time()),
            labels=labels,
            comment=comment,
            text=text,
        ))
    return jsonify({
        'comment': comment,
        'labels': labels
    })


@app.route('/api/history', methods=['GET'])
def api_history():
    '''Retrieve the latest history items with an optional limit.
    '''
    limit = int(request.args.get('limit', 20))
    history = [x._asdict() for x in get_db().get_many(limit)]
    return jsonify(history)


@app.route('/api/export', methods=['GET'])
def api_export():
    '''Download the complete analysis history as a CSV file.
    '''
    with io.StringIO() as f:
        writer = csv.DictWriter(f, fieldnames=Record._fields)
        writer.writeheader()
        for row in (x._asdict() for x in get_db().get_many()):
            writer.writerow({**row, **{'labels':', '.join(row['labels'])}})
        return send_file(io.BytesIO(f.getvalue().encode('utf-8')),
            as_attachment=True,
            download_name='export.csv',
            mimetype='text/csv'
        )
