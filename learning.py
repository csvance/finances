from schema import *
from sqlalchemy import literal


class LearnRules(object):
    def __init__(self):
        self.session = Session()

    def _print_rules(self,rules):

        index = 1
        for rule in rules:
            print("%d: %s" % (index,rule))
            index += 1

    def run(self):

        session = self.session

        rules = session.query(TransactionRule).order_by(TransactionRule.name).all()

        transactions = session.query(Transaction).filter(Transaction.rule_id == None).all()
        for transaction in transactions:

            # Check for a match
            match = session.query(TransactionRuleMatch).filter(literal(transaction.desc).contains(TransactionRuleMatch.match)).first()
            if match is not None:
                transaction.rule_id = match.transaction_rule_id
                continue

            # Assign a rule and create a match
            self._print_rules(rules)

            print(transaction)
            rule_index = int(input("rule> "))

            if rule_index > 0:
                transaction.rule_id = rules[rule_index-1].id
            else:
                continue

            m = input("match> ")

            if m != "":
                match = TransactionRuleMatch(match=m,transaction_rule_id=transaction.rule_id)
                session.add(match)

            session.commit()

        session.commit()
