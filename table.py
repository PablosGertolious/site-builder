import re

class Table:
    def __init__(self,migration):

        # Get table name from the migration file
        migration = migration.replace(" ","")
        pattern = re.compile(".+Schema::create\(\'(?P<table_name>\w+)\'.+")
        match = (pattern.match(migration))['table_name']

        if match is not None:
            self.table_name = (pattern.match(migration))['table_name']
        else:
            table_name = input("What is the table name: ")
            table = Table(table_name)

        # self.table_name_singular = input('What is the singular of the table name? ')
        self.table_name_singular = 'country'

        # get the attributes of the table from the migration file
        self.obj_name = []
        self.obj_key = []
        self.attrs = {}
        list = migration.replace(" ","").split("$table->")[1:]
        pattern_text = r'(?P<type>\w+)\((?P<arg>(.+)?)\)'
        pattern = re.compile(pattern_text)
        for j in range(len(list)):
            calls = list[j].split("->")
            for i in range(len(calls)):
                match = pattern.match(calls[i])

                if match is not None:
                    if match['type'] in ['string','boolean','text']:
                        # self.attrs.append([match['arg'],match['type']])
                        self.attrs[match['arg'].replace("'","")] = match['type']

        # What is the name of each object?
        if "name" in self.attrs:
            self.obj_name = self.attrs["name"]
        else:
            self.obj_name = input("What is the name of each table entry:")

        # What is the name of each object?
        if "slug" in self.attrs:
            self.obj_key = "slug"
        else:
            self.obj_key = "id"



    def create_model(self):
        # Create model
        model_text = "<?php\n\nnamespace App;\n\nuse Illuminate\Database\Eloquent\Model;\nuse Illuminate\Support\Facades\DB;"

        # If softDeletes
        if False:
            model_text+="use Illuminate\Database\Eloquent\SoftDeletes;"
        model_text+="\n\n/**\n * @property string id The ID of this collective.\n */\nclass "
        model_text+=self.table_name_singular.capitalize()
        model_text+="extends Model\n{\n   "
        # If softDeletes
        if False:
            model_text+="use SoftDeletes;\n"
        model_text+="\n    protected $dates = ["
        # If softDeletes, times statmps
        dates=""
        if False:
            dates+="'deleted_at'"
            if False:
                dates+=","
        if False:
            dates+="'created_at',"
            dates+="'modified_at'"
        model_text+=dates
        model_text+='];\nprotected $fillable = ['
        # model_text+=
        attrs = list(self.attrs.keys())

        for i in range(len(attrs)):
            model_text+=("'" + attrs[i] + "'")
            if i != len(attrs)-1:
                model_text+=","
        model_text+="];\n\n// By default, we won't show these in the JSON representation.\nprotected $hidden = ["
        model_text+=dates
        model_text+="];\nprotected $guarded = array();\n\n\npublic static function boot()\n{\n    parent::boot();\n\n    "

        if self.obj_key=='slug':
            model_text+="static::creating(function ($model) {\n\n    $tempSlug = $model->name;\n\n    $model->slug = str_slug($tempSlug);// change the ToBeSluggiefied\n\n    $baseSlug =\n        static::whereRaw(\"slug = '$model->slug'\")\n            ->latest('id')\n            ->value('slug');\n\n    if ($baseSlug) {\n      $latestSlug =\n          static::whereRaw(\"(slug = '$model->slug' or slug LIKE '$model->slug-%')\")\n              ->latest('id')\n              ->value('slug');\n        if ($latestSlug) {\n            $pieces = explode('-', $latestSlug);\n\n            $number = intval(end($pieces));\n\n            $model->slug .= '-' . ($number + 1);\n        } else {\n            $model->slug .= '-1';\n        }\n    }\n});\n\nstatic::updating(function ($model) {\n\n    // Only do the slug check if changing\n    $newSlug = str_slug($model->name);\n    if ($model->slug != $newSlug) {\n        $model->slug = $newSlug;\n\n        $baseSlug =\n          static::whereRaw(\"id!=$model->id AND slug = '$model->slug'\")\n              ->latest('id')\n              ->value('slug');\n\n        if ($baseSlug) {\n          $latestSlug =\n            static::whereRaw(\"id!=$model->id AND slug LIKE '$model->slug-%'\")\n                ->latest('id')\n                ->value('slug');\n            if ($latestSlug) {\n                $pieces = explode('-', $latestSlug);\n\n                $number = intval(end($pieces));\n\n                $model->slug .= '-' . ($number + 1);\n            } else {\n                $model->slug .= '-1';\n            }\n        }\n    }\n});"

        model_text+="\n\n}\n\n}\n"

        text_file = open(self.table_name_singular.capitalize()+".php", "w")
        text_file.write(model_text)
        text_file.close()

# def draw_environment(blobs):
#     game_display.fill(WHITE)
#     for blob_id in blobs:
#         blob = blobs[blob_id]
#         pygame.draw.circle(game_display, blob.color, [blob.x,blob.y], blob.size)
#         blob.move()
#     pygame.display.update()
#
#
# def main():
#     blue_blobs = dict(enumerate([Blob(BLUE) for i in range(STARTING_BLUE_BLOBS)]))
#     red_blobs = enumerate([Blob(RED) for i in range(STARTING_RED_BLOBS)])
#     print(red_blobs)
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#
#         draw_environment(blue_blobs)
#         clock.tick(60)
#
# if __name__ == '__main__':
#     main()
