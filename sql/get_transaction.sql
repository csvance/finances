select strftime('%m',"transaction".date)||'/1/'||strftime('%Y',"transaction".date),"transaction".desc,transaction_category.name,transaction_tag.name,"transaction".amount from "transaction",transaction_rule,transaction_category,transaction_tag,transaction_ruletag
where "transaction".rule_id = transaction_rule.id AND
transaction_rule.category_id = transaction_category.id AND
transaction_ruletag.transaction_rule_id = transaction_rule.id AND
transaction_tag.id = transaction_ruletag.tag_id AND
transaction_tag."primary"
order by date desc