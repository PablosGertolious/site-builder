from table import *

table = Table('RED','slug')
['attr','type','nullable']
table.edit_attrs.append(['test','nullable','text'])
table.edit_attrs.append(['slug','required','string'])
table.edit_attrs.append(['softDeletes'])
print(table.edit_attrs)
