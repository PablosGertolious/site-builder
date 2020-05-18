import re
import os


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
            self.obj_name = "name"
        else:
            self.obj_name = input("What is the name of each table entry:")

        # What is the name of each object?
        if "slug" in self.attrs:
            self.obj_key = "slug"
        else:
            self.obj_key = "id"

    def create_model(self):
        # Create model
        code = "<?php\n\nnamespace App;\n\nuse Illuminate\Database\Eloquent\Model;\nuse Illuminate\Support\Facades\DB;"

        # If softDeletes
        if False:
            code+="use Illuminate\Database\Eloquent\SoftDeletes;"
        code+="\n\n/**\n * @property string id The ID of this collective.\n */\nclass "
        code+=self.table_name_singular.capitalize()
        code+="extends Model\n{\n   "
        # If softDeletes
        if False:
            code+="use SoftDeletes;\n"
        code+="\n    protected $dates = ["
        # If softDeletes, times statmps
        dates=""
        if False:
            dates+="'deleted_at'"
            if False:
                dates+=","
        if False:
            dates+="'created_at',"
            dates+="'modified_at'"
        code+=dates
        code+='];\nprotected $fillable = ['
        attrs = list(self.attrs.keys())

        for i in range(len(attrs)):
            code+=("'" + attrs[i] + "'")
            if i != len(attrs)-1:
                code+=","
        code+="];\n\n// By default, we won't show these in the JSON representation.\nprotected $hidden = ["
        code+=dates
        code+="];\nprotected $guarded = array();\n\n\npublic static function boot()\n{\n    parent::boot();\n\n    "

        if self.obj_key=='slug':
            code+="static::creating(function ($model) {\n\n    $tempSlug = $model->{obj_name};\n\n    $model->slug = str_slug($tempSlug);// change the ToBeSluggiefied\n\n    $baseSlug =\n        static::whereRaw(\"slug = '$model->slug'\")\n            ->latest('id')\n            ->value('slug');\n\n    if ($baseSlug) {\n      $latestSlug =\n          static::whereRaw(\"(slug = '$model->slug' or slug LIKE '$model->slug-%')\")\n              ->latest('id')\n              ->value('slug');\n        if ($latestSlug) {\n            $pieces = explode('-', $latestSlug);\n\n            $number = intval(end($pieces));\n\n            $model->slug .= '-' . ($number + 1);\n        } else {\n            $model->slug .= '-1';\n        }\n    }\n});\n\nstatic::updating(function ($model) {\n\n    // Only do the slug check if changing\n    $newSlug = str_slug($model->{obj_name});\n    if ($model->slug != $newSlug) {\n        $model->slug = $newSlug;\n\n        $baseSlug =\n          static::whereRaw(\"id!=$model->id AND slug = '$model->slug'\")\n              ->latest('id')\n              ->value('slug');\n\n        if ($baseSlug) {\n          $latestSlug =\n            static::whereRaw(\"id!=$model->id AND slug LIKE '$model->slug-%'\")\n                ->latest('id')\n                ->value('slug');\n            if ($latestSlug) {\n                $pieces = explode('-', $latestSlug);\n\n                $number = intval(end($pieces));\n\n                $model->slug .= '-' . ($number + 1);\n            } else {\n                $model->slug .= '-1';\n            }\n        }\n    }\n});"

        code+="\n\n}\n\n}\n"

        text_file = open(self.table_name_singular.capitalize()+".php", "w")
        text_file.write(code)
        text_file.close()

    def create_admin(self):
        table_name = self.table_name
        table_name = self.table_name
        var_name = self.table_name_singular
        table_headline = self.table_name.replace("_"," ").title()
        obj_key = self.obj_key
        obj_name = self.obj_name

        try:
            os.mkdir(self.table_name)
        except OSError:
            print ("Creation of the directory %s failed. (make sure it doesn't already exist)" % self.table_name)
        else:
            print ("Successfully created the directory %s " % self.table_name)

        code = f"@extends('layouts.admin')\n\n@section('content')\n\n  @if (isset(${var_name}))\n    {{!! Form::model(${var_name}, array('url' => url('admin/{table_name}/' .${var_name}->{obj_key} . '/edit'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}}\n  @else\n    {{!! Form::open(array('url' => url('admin/{table_name}/create'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}}\n  @endif\n\n  <div class=\"row\">\n    <div class=\"col-12 \">\n      <div class=\"page-header\">\n        <ol class=\"breadcrumb\">\n          <li class=\"breadcrumb-item\"><a href=\"/admin\">Home</a></li>\n          <li class=\"breadcrumb-item\"><a href=\"/admin/{table_name}\">{table_name}</a></li>\n  @if (isset(${var_name}))\n          <li class=\"breadcrumb-item\"><a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}\">{{{{ ${var_name}->{obj_name} }}}}</a></li>\n          <li class=\"breadcrumb-item active\">Edit</li>\n  @else\n          <li class=\"breadcrumb-item active\">Create</li>\n  @endif\n        </ol>\n\n        <div class=\"float-right\">\n          <div class=\"btn-group\" role=\"group\">\n            <a href=\"/admin/{table_name}\" class=\"btn btn-secondary\"><i class=\"fas fa-chevron-left fa-fw\" aria-hidden=\"true\"></i> Back</a>\n          </div>\n          <button type=\"submit\" class=\"btn btn-primary\">Save</button>\n        </div>\n\n        <h1>@if (isset(${var_name})) Edit @else Create @endif {table_headline}</h1>\n    </div>\n    </div>\n  </div>\n\n  <!-- Display any alerts -->\n  @include('components.alerts')\n\n  <div class=\"row\">\n    <div class=\"col-12\">\n \n"

        for attr in self.attrs:
            attr_title = attr.replace("_"," ").title()
            if attr == self.obj_name:
                code += f"<div class=\"form-group\">\n  {{!! Form::label('{attr_title}') !!}}\n  {{!! Form::text('{attr}', null,\n      array('required',\n            'class'=>'form-control slugpart slugpart-1',\n            'placeholder'=>'{attr_title}')) !!}}\n</div>\n"
                continue
            if attr == "slug":
                code += f"\n        <div class=\"row\">\n          <div class={{!! (isset(${var_name}) ? \"col-11\":\"col-12\") !!}}>\n            <div class=\"form-group\">\n              {{!! Form::label('Slug') !!}}\n              {{!! Form::text('slug', null,\n                array('class'=>'form-control',\n                      'id'=>'slug',\n                      'placeholder'=>'Slug')) !!}}\n            </div>\n          </div>\n        @if (isset(${var_name}))\n\n          <div class=\"col-1\">\n            <label>&nbsp;</label><br />\n            <button type=\"button\" class=\"btn btn-block btn-secondary\" id=\"slugUnlockToggle\" data-toggle=\"modal\" data-target=\"#slugUnlockModal\"><i class=\"fa fa-unlock\"></i></button>\n            <div id=\"slugUnlockModal\" class=\"modal\" tabindex=\"-1\" role=\"dialog\">\n              <div class=\"modal-dialog\" role=\"document\">\n                <div class=\"modal-content\">\n                  <div class=\"modal-header\">\n                    <h5 class=\"modal-title\">Unlock Slug?</h5>\n                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n                  </div>\n                  <div class=\"modal-body\">\n                    <p>Changes to the slug can may break existing links and negatively impact Search Engine Optimization (SEO).</p>\n                    <p>Are you sure you want to change the slug?</p>\n                  </div>\n                  <div class=\"modal-footer\">\n                    <button type=\"button\" class=\"btn btn-secondary\" data-dismiss=\"modal\">Cancel</button>\n                    <button type=\"button\" id=\"slugUnlock\" class=\"btn btn-primary\" data-dismiss=\"modal\">Yes, Unlock</button>\n                  </div>\n                </div>\n              </div>\n            </div>\n          </div>\n        @endif\n\n        </div>\n"
                continue
            if(self.attrs[attr]=="string"):
                code+=f"<div class=\"form-group\">\n  {{!! Form::label('{attr_title}') !!}}\n  {{!! Form::text('{attr}', null,\n      array('required',\n            'class'=>'form-control',\n            'placeholder'=>'{attr_title}')) !!}}\n</div>\n"
                continue
            if(self.attrs[attr]=="text"):
                code+=f"\n        <div class=\"form-group\">\n          {{!! Form::label('{attr_title}') !!}}\n          {{!! Form::textarea('{attr}', ( isset(${var_name}->{attr}) ? ${var_name}->{attr} : null ),\n              array('class'=>'form-control',\n                    'placeholder'=>'{attr_title}')) !!}}\n        </div>\n"
                continue
            if(self.attrs[attr]=="boolean"):
                code+=f"\n        <label>{attr_title}</label>\n        <div class=\"form-group\">\n          <div class=\"form-check form-check-inline\">\n            <input class=\"form-check-input\" type=\"radio\" name=\"{attr}\" id=\"{attr}-yes\" value=\"true\" required=\"required\" @if (isset(${var_name})) @if (${var_name}->{attr} == true) checked=\"checked\" @endif @else checked=\"checked\" @endif >\n            <label class=\"form-check-label\" for=\"{attr}-yes\">Yes</label>\n          </div>\n          <div class=\"form-check form-check-inline\">\n            <input class=\"form-check-input\" type=\"radio\" name=\"{attr}\" id=\"{attr}-no\" value=\"false\" required=\"required\" @if (isset(${var_name}) && ${var_name}->{attr} == false) checked=\"checked\" @endif >\n            <label class=\"form-check-label\" for=\"{attr}-no\">No</label>\n          </div>\n        </div>\n"
                continue
            print("Did not add field for "+ self.attrs)
        code+=f"\n        <div class=\"form-group\">\n          @if (isset(${var_name}))\n            <a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}/delete\" class=\"btn btn-outline-danger float-right\">Delete</a>\n          @endif\n            {{!! Form::submit('Save',array('class'=>'btn btn-primary')) !!}}\n\n        </div>\n\n    </div>\n  </div>\n\n  {{!! Form::close() !!}}\n\n\n@endsection\n"

        text_file = open(self.table_name + "/create_edit.blade.php", "w")
        text_file.write(code)
        text_file.close()

        code = f"@extends('layouts.admin')\n\n@section('content')\n\n  <div class=\"row\">\n    <div class=\"col-12 \">\n      <div class=\"page-header\">\n        <ol class=\"breadcrumb\">\n          <li class=\"breadcrumb-item\"><a href=\"/admin\">Home</a></li>\n          <li class=\"breadcrumb-item\"><a href=\"/admin/{table_name}\">{table_headline}</a></li>\n          <li class=\"breadcrumb-item\"><a href=\"/admin/{table_name}/{{{{${var_name}->{obj_key}}}}}\">{{{{${var_name}->{obj_name}}}}}</a></li>\n          <li class=\"breadcrumb-item active\">Delete</li>\n        </ol>\n\n        <div class=\"float-right\">\n          <div class=\"btn-group\" role=\"group\">\n            <a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}\" class=\"btn btn-secondary\"><i class=\"fas fa-chevron-left fa-fw\" aria-hidden=\"true\"></i> Back</a>\n          </div>\n        </div>\n\n        <h1>{table_headline} Delete</h1>\n    </div>\n    </div>\n  </div>\n\n  <!-- Display any alerts -->\n  @include('components.alerts')\n\n  <div class=\"row\">\n    <div class=\"col-12\">\n      {{!! Form::model(${var_name}, array('url' => url('admin/{table_name}/' .${var_name}->{obj_key} . '/delete'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}}\n        <p>Are you sure you want to delete the {table_headline}: <strong>{{{{ ${var_name}->{obj_name} }}}}</strong>?</p>\n        <p>Deletion is permanent and cannot be reversed.</p>\n\n        <div class=\"form-group\">\n            {{!! Form::submit('Yes, Delete',array('class'=>'btn btn-danger')) !!}}\n            <a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}\" class=\"btn btn-secondary\">Cancel</a>\n        </div>\n\n      {{!! Form::close() !!}}\n\n    </div>\n  </div>\n\n@endsection\n"

        text_file = open(self.table_name + "/delete.blade.php", "w")
        text_file.write(code)
        text_file.close()

        code = f"@extends('layouts.admin')\n\n@section('content')\n\n  <div class=\"row\">\n    <div class=\"col-12\">\n      <div class=\"page-header\">\n        <ol class=\"breadcrumb\">\n          <li class=\"breadcrumb-item\"><a href=\"/admin\">Home</a></li>\n          <li class=\"breadcrumb-item active\">{table_headline}</li>\n        </ol>\n\n        <div class=\"float-right\">\n          <div class=\"btn-group\" role=\"group\">\n            <a href=\"/admin/{table_name}/create\" class=\"btn btn-secondary\"><i class=\"fas fa-plus\" aria-hidden=\"true\"></i> Add New</a>\n          </div>\n        </div>\n\n        <h1>{table_headline} <i class=\"fas fa-filter filter-toggle\" aria-hidden=\"true\" data-toggle=\"collapse\" data-target=\"#filterCollapse\" aria-expanded=\"false\" aria-controls=\"filterCollapse\"></i></h1>\n      </div>\n    </div>\n  </div>\n\n  <!-- Display any alerts -->\n  @include('components.alerts')\n\n  <div class=\"row\">\n    <div class=\"col-12\">\n      <div class=\"cardx bg-light mb-1 collapse @if ($hasFilter) show @endif\" id=\"filterCollapse\">\n        <div class=\"card-body\">\n          <form action=\"/admin/{table_name}\" method=\"get\" class=\"filters-form\">\n            <div class=\"row\">\n              <div class=\"col-12 col-md-3\">\n                <label class=\"sr-only\" for=\"name\">Name </label>\n                <input type=\"text\" class=\"form-control mr-1\" id=\"name\" name=\"name\" placeholder=\"Name\" value=\"@if (array_key_exists('name',$filters)){{{{ $filters['name'] }}}}@endif\">\n              </div>\n              <div class=\"col-12 col-md-3\">\n                <button type=\"submit\" class=\"btn btn-primary mr-1\"><i class=\"fa fa-filter\"></i></button>\n                <a href=\"/admin/{table_name}\" class=\"btn btn-secondary\"><i class=\"fa fa-times\"></i></a>\n                <input type=\"hidden\" id=\"sort-column\" name=\"sort-column\" value=\"@if (array_key_exists('sort-column',$filters)){{{{ $filters['sort-column'] }}}}@else{{{{'name'}}}}@endif\" />\n                <input type=\"hidden\" id=\"sort-order\" name=\"sort-order\" value=\"@if (array_key_exists('sort-order',$filters)){{{{ $filters['sort-order'] }}}}@else{{{{'asc'}}}}@endif\" />\n              </div>\n            </div>\n\n        </div>\n      </div>\n      <table class=\"table table-sm table-striped table-sortable\">\n        <thead class=\"thead-inverse\">\n          <tr>\n            <th class=\"sortable-toggle\" data-column=\"name\">Name</th>\n            <th></th>\n          </tr>\n        </thead>\n        <tbody>\n@if (count(${table_name}) > 0)\n  @foreach (${table_name} as ${var_name})\n          <tr>\n            <td><a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}\" class=\"btn btn-sm btn-link\">{{{{ ${var_name}->{obj_name}  }}}}</a></td>\n            <td><a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}\" class=\"btn btn-sm btn-link\">{{{{ ${var_name}->is_published ? 'Yes' : 'No' }}}}</a></td>\n            <td class=\"text-right\">\n              <div class=\"btn-group\">\n                <a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}\" class=\"btn btn-primary btn-sm\">\n                  View\n                </a>\n                <button type=\"button\" class=\"btn btn-sm btn-primary dropdown-toggle dropdown-toggle-split\" data-toggle=\"dropdown\" aria-haspopup=\"true\" aria-expanded=\"false\">\n                  <span class=\"sr-only\">Toggle Dropdown</span>\n                </button>\n                <div class=\"dropdown-menu dropdown-menu-right\">\n                  <a href=\"/admin/{table_name}/{{{{ ${var_name}->{obj_key} }}}}/edit\" class=\"dropdown-item\">Edit</a>\n                </div>\n              </div>\n            </td>\n          </tr>\n  @endforeach\n@else\n          <tr>\n            <td colspan=\"3\" class=\"text-center\">No {table_name} found. Why not <a href=\"/admin/{table_name}/create\">create the first one</a>?</td>\n          </tr>\n@endif\n        </tbody>\n      </table>\n    </div>\n  </div>\n\n@endsection\n"

        text_file = open(self.table_name + "/list.blade.php", "w")
        text_file.write(code)
        text_file.close()

        code = f"@extends('layouts.admin')\n\n@section('content')\n\n  <div class=\"row\">\n    <div class=\"col-12\">\n      <div class=\"page-header\">\n        <ol class=\"breadcrumb\">\n          <li class=\"breadcrumb-item\"><a href=\"/admin\">Home</a></li>\n          <li class=\"breadcrumb-item\"><a href=\"/admin/posts\">Blog</a></li>\n          <li class=\"breadcrumb-item\"><a href=\"/admin/{table_name}\">{table_headline}</a></li>\n          <li class=\"breadcrumb-item active\">{{{{${var_name}->{obj_name}}}}}</li>\n        </ol>\n\n        <div class=\"float-right\">\n          <div class=\"btn-group\" role=\"group\">\n            <a href=\"/admin/{table_name}\" class=\"btn btn-secondary\"><span class=\"fas fa-chevron-left\"></span> Back</a>\n            <a href=\"/admin/{table_name}/{{{{${var_name}->{obj_key}}}}}/edit\" class=\"btn btn-secondary\"> Edit</a>\n          </div>\n        </div>\n\n        <h1>{{{{${var_name}->{obj_name}}}}}</h1>\n      </div>\n    </div>\n  </div>\n\n  <!-- Display any alerts -->\n  @include('components.alerts')\n\n\n\n@endsection\n"

        text_file = open(self.table_name + "/view.blade.php", "w")
        text_file.write(code)
        text_file.close()
