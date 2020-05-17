import re
from table import *

with open('example_migration.php', 'r') as file:
    string = file.read().replace('\n', '').replace(' ','')

table = Table(string)

table.create_model()

import os

try:
    os.mkdir(table.table_name)
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)

# create admin files
    # This could be messy. I want avoid this getting to detailed.
