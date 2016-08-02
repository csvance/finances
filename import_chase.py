import csv
from dateutil.parser import parse as date_parse
from schema import *


class ImportChase(object):

    def __init__(self, path, starting_date):
        self.path = path
        self.session = Session()
        self.starting_date = starting_date

    def handle_row(self, dict):

        session = self.session
        type_id = None

        type = session.query(TransactionType).filter(TransactionType.name == dict['Type']).first()
        if type is None:

            type = TransactionType(name=dict['Type'])
            session.add(type)
            session.commit()
            type_id = type.id
        else:
            type_id = type.id

        day = date_parse(dict['Posting Date'])
        if day < self.starting_date:
            return

        transaction = Transaction()
        transaction.desc = dict['Description']
        transaction.amount = dict['Amount']
        transaction.balance = dict['Balance']
        transaction.date = day
        transaction.type_id = type_id
        transaction.generate_hash()

        if session.query(Transaction).filter(Transaction.hash == transaction.hash).first() is None:
            session.add(transaction)
        else:
            # Data is sorted in descending order, so stop at first known transaction match
            return

    def run(self):

        # Read csv file into dictionary
        reader = csv.DictReader(open(self.path,'r'))
        for row in reader:
            self.handle_row(row)

        self.session.commit()