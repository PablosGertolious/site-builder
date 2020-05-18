import re
from table import *

with open('example_migration.php', 'r') as file:
    string = file.read().replace('\n', '').replace(' ','')

table = Table(string)

table.create_model()

table.create_admin()
