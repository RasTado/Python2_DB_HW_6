import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Stock, Sale
import json


DSN = 'postgresql://postgres:postgres@localhost:5432/netology_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('fixtures/tests_data.json', 'r') as f:
    json_data = json.load(f)

for record in json_data:
    model = {
        'publisher': Publisher,
        'book': Book,
        'shop': Shop,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


publisher_search = input('Input name publisher or id: ')

query_1 = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == publisher_search)
query_2 = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher_search)
shops = []

try:
    result = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.id == int(publisher_search))
except ValueError:
    result = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher_search)
for i in result:
    shops.append(i.name)

print(f'Books publisher {publisher_search} in shops: \n{shops}')

session.close()