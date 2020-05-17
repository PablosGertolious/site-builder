import re

string = "$table->bigIncrements('id');$table->string('name');$table->string('slug');$table->string('abbreviation');$table->string('code');$table->boolean('is_active')->default(true);$table->timestamps();$table->softDeletes();"

print(string.find("string")>1)
