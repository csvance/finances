from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, Boolean, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session
from sqlalchemy import create_engine
import hashlib

Base = declarative_base()


class TransactionCategory(Base):
    __tablename__ = "transaction_category"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return self.name


class TransactionTag(Base):
    __tablename__ = "transaction_tag"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    primary = Column(Boolean, nullable=False, default=True)

    def __repr__(self):
        return self.name


class TransactionType(Base):
    __tablename__ = "transaction_type"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return self.name


class Transaction(Base):
    __tablename__ = "transaction"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    balance = Column(Float)
    desc = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    type_id = Column(Integer, ForeignKey('transaction_type.id'), nullable=False)
    type = relationship('TransactionType')
    rule_id = Column(Integer, ForeignKey('transaction_rule.id'))
    rule = relationship('TransactionRule')

    def __repr__(self):
        return "Date: %s Amount: %f Description: %s" % (self.date, self.amount, self.desc)

    def generate_hash(self):
        hash_input = (str(self.date) + str(self.amount) + str(self.balance) + str(self.desc)).encode('utf-8')
        h = hashlib.md5()
        h.update(hash_input)
        self.hash = h.digest()


class TransactionRuleMatch(Base):
    __tablename__ = "transaction_rule_match"

    id = Column(Integer, primary_key=True)
    match = Column(String, nullable=False)
    transaction_rule_id = Column(Integer, ForeignKey('transaction_rule.id'), nullable=False)
    transaction_rule = relationship('TransactionRule')


class TransactionRule(Base):
    __tablename__ = "transaction_rule"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('transaction_category.id'), nullable=False)
    category = relationship("TransactionCategory")

    def __repr__(self):
        return self.name


class TransactionRuleTag(Base):
    __tablename__ = "transaction_ruletag"

    id = Column(Integer, primary_key=True)
    transaction_rule_id = Column(Integer, ForeignKey('transaction_rule.id'), nullable=False)
    transaction_rule = relationship('TransactionRule')
    tag_id = Column(Integer, ForeignKey('transaction_tag.id'), nullable=False)
    tag = relationship('TransactionTag')


engine = create_engine('sqlite:///finances.db')
Base.metadata.create_all(engine)

session_factory = sessionmaker(autoflush=False)
session_factory.configure(bind=engine)
Session = scoped_session(session_factory)

if True:
    session = Session()

    rules = {'Regular': ['ISP', 'Cell Phone', 'Internet Services', 'Car Insurance', 'Gas', 'Electricity', 'Rent',
                         'Medical Insurance', 'School Supplies', 'Tuition', 'Groceries'],
             'Irregular': ['Pet', 'Car Repair', 'Medical', 'Dental', 'Personal Care'],
             'Extra': ['Eating Out', 'Entertainment', 'Hobby', 'Political', 'Charity', 'Travel'],
             'Income': ['Job', 'Family', 'Services']}

    for category_name in rules:

        category = session.query(TransactionCategory).filter(TransactionCategory.name == category_name).first()
        if category is None:
            category = TransactionCategory(name=category_name)
            session.add(category)
            session.commit()

        for tag_name in rules[category_name]:

            tag = session.query(TransactionTag).filter(TransactionTag.name == tag_name).first()
            if tag is None:
                tag = TransactionTag(name=tag_name, primary=True)
                session.add(tag)

            rule = session.query(TransactionRule).filter(TransactionRule.name == tag_name).first()
            if rule is None:
                rule = TransactionRule(name=tag_name, category_id=category.id)
                session.add(rule)

            session.commit()

            if session.query(TransactionRuleTag).filter(and_(TransactionRuleTag.tag_id == tag.id,
                                                             TransactionRuleTag.transaction_rule_id == rule.id)).first() is None:
                ruletag = TransactionRuleTag(tag_id=tag.id, transaction_rule_id=rule.id)
                session.add(ruletag)

    session.commit()
