import json
import sqlite3
from typing import NamedTuple, Optional, Iterable
from .config import DATABASE_PATH


class Record(NamedTuple):
    created_at:int
    labels:list[str]
    comment:str
    text:str

    @classmethod
    def from_json(cls, serialized:str):
        x = json.loads(serialized)
        return cls(
            created_at=x['created_at'],
            labels=x['labels'],
            comment=x['comment'],
            text=x['text']
        )

    def serialize(self) -> str:
        return json.dumps({
            'created_at': self.created_at,
            'labels': self.labels,
            'comment': self.comment,
            'text': self.text
        })


class Database:
    def __init__(self):
        self.db = sqlite3.connect(DATABASE_PATH)
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS records (
                created_at INTEGER,
                record TEXT
            )
        ''')
        self.db.commit()

    def put(self, record:Record):
        '''Put a Record into the database.
        '''
        self.db.execute('''
            INSERT INTO RECORDS (created_at, record)
            VALUES (?, ?)
        ''', [record.created_at, record.serialize()])
        self.db.commit()

    def get_many(self, limit:Optional[int]=None) -> Iterable[Record]:
        '''Query last Records optionally limited by limit argument.
        '''
        query_limit = f'LIMIT {int(limit)}' if limit else ''
        cur = self.db.execute(f'''
            SELECT created_at, record FROM records
            ORDER BY created_at DESC {query_limit}
        ''')
        for _, record in cur:
            yield Record.from_json(record)
