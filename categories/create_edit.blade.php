@extends('layouts.admin')

@section('content')

  @if (isset(${var_name}))
    {{!! Form::model(${var_name}, array('url' => url('admin/{table_name}/' .${var_name}->{key} . '/edit'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}}
  @else
    {{!! Form::open(array('url' => url('admin/{table_name}/create'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}}
  @endif

  <div class="row">
    <div class="col-12 ">
      <div class="page-header">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
          <li class="breadcrumb-item"><a href="/admin/{table_name}">{table_name}</a></li>
  @if (isset(${var_name}))
          <li class="breadcrumb-item"><a href="/admin/{table_name}/{{{{ ${var_name}->{key} }}}}">{{{{ ${var_name}->name }}}}</a></li>
          <li class="breadcrumb-item active">Edit</li>
  @else
          <li class="breadcrumb-item active">Create</li>
  @endif
        </ol>

        <div class="float-right">
          <div class="btn-group" role="group">
            <a href="/admin/{table_name}" class="btn btn-secondary"><i class="fas fa-chevron-left fa-fw" aria-hidden="true"></i> Back</a>
          </div>
          <button type="submit" class="btn btn-primary">Save</button>
        </div>

        <h1>@if (isset(${var_name})) Edit @else Create @endif {table_headline}</h1>
    </div>
    </div>
  </div>

  <!-- Display any alerts -->
  @include('components.alerts')

  <div class="row">
    <div class="col-12">


        <div class="form-group">
          {{!! Form::label('Name') !!}}
          {{!! Form::text('name', null,
              array('required',
                    'class'=>'form-control slugpart slugpart-1',
                    'placeholder'=>'Name')) !!}}
        </div>

        <div class="row">
          <div class={{!! (isset(${var_name}) ? "col-11":"col-12") !!}}>
            <div class="form-group">
              {{!! Form::label('Slug') !!}}
              {{!! Form::text('slug', null,
                array('class'=>'form-control',
                      'id'=>'slug',
                      'placeholder'=>'Slug')) !!}}
            </div>
          </div>
        @if (isset(${var_name}))

          <div class="col-1">
            <label>&nbsp;</label><br />
            <button type="button" class="btn btn-block btn-secondary" id="slugUnlockToggle" data-toggle="modal" data-target="#slugUnlockModal"><i class="fa fa-unlock"></i></button>

            <div id="slugUnlockModal" class="modal" tabindex="-1" role="dialog">
              <div class="modal-dialog" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">Unlock Slug?</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                  </div>
                  <div class="modal-body">
                    <p>Changes to the slug can may break existing links and negatively impact Search Engine Optimization (SEO).</p>
                    <p>Are you sure you want to change the slug?</p>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button type="button" id="slugUnlock" class="btn btn-primary" data-dismiss="modal">Yes, Unlock</button>
                  </div>
                </div>
              </div>
            </div>

          </div>
        @endif

        </div>

        <div class="form-group">
          {{!! Form::label('Description') !!}}
          {{!! Form::textarea('description', ( isset(${var_name}->description) ? ${var_name}->description : null ),
              array('class'=>'form-control',
                    'placeholder'=>'{table_name} Description')) !!}}
        </div>

        <label>Published</label>
        <div class="form-group">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="is_published" id="is_published-yes" value="true" required="required" @if (isset(${var_name})) @if (${var_name}->is_published == true) checked="checked" @endif @else checked="checked" @endif >
            <label class="form-check-label" for="is_published-yes">Yes</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="is_published" id="is_published-no" value="false" required="required" @if (isset(${var_name}) && ${var_name}->is_published == false) checked="checked" @endif >
            <label class="form-check-label" for="is_published-no">No</label>
          </div>
        </div>

        <div class="form-group">
          @if (isset(${var_name}))
            <a href="/admin/{table_name}/{{{{ ${var_name}->{key} }}}}/delete" class="btn btn-outline-danger float-right">Delete</a>
          @endif
            {{!! Form::submit('Save',array('class'=>'btn btn-primary')) !!}}

        </div>

    </div>
  </div>

  {{!! Form::close() !!}}


@endsection
