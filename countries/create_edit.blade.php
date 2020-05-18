@extends('layouts.admin')

@section('content')

  @if (isset($country))
    {!! Form::model($country, array('url' => url('admin/countries/' .$country->slug . '/edit'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}
  @else
    {!! Form::open(array('url' => url('admin/countries/create'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}
  @endif

  <div class="row">
    <div class="col-12 ">
      <div class="page-header">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
          <li class="breadcrumb-item"><a href="/admin/countries">countries</a></li>
  @if (isset($country))
          <li class="breadcrumb-item"><a href="/admin/countries/{{ $country->slug }}">{{ $country->name }}</a></li>
          <li class="breadcrumb-item active">Edit</li>
  @else
          <li class="breadcrumb-item active">Create</li>
  @endif
        </ol>

        <div class="float-right">
          <div class="btn-group" role="group">
            <a href="/admin/countries" class="btn btn-secondary"><i class="fas fa-chevron-left fa-fw" aria-hidden="true"></i> Back</a>
          </div>
          <button type="submit" class="btn btn-primary">Save</button>
        </div>

        <h1>@if (isset($country)) Edit @else Create @endif Countries</h1>
    </div>
    </div>
  </div>

  <!-- Display any alerts -->
  @include('components.alerts')

  <div class="row">
    <div class="col-12">
 
<div class="form-group">
  {!! Form::label('Name') !!}
  {!! Form::text('name', null,
      array('required',
            'class'=>'form-control slugpart slugpart-1',
            'placeholder'=>'Name')) !!}
</div>

        <div class="row">
          <div class={!! (isset($country) ? "col-11":"col-12") !!}>
            <div class="form-group">
              {!! Form::label('Slug') !!}
              {!! Form::text('slug', null,
                array('class'=>'form-control',
                      'id'=>'slug',
                      'placeholder'=>'Slug')) !!}
            </div>
          </div>
        @if (isset($country))

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
  {!! Form::label('Abbreviation') !!}
  {!! Form::text('abbreviation', null,
      array('required',
            'class'=>'form-control',
            'placeholder'=>'Abbreviation')) !!}
</div>
<div class="form-group">
  {!! Form::label('Code') !!}
  {!! Form::text('code', null,
      array('required',
            'class'=>'form-control',
            'placeholder'=>'Code')) !!}
</div>

        <label>Is Active</label>
        <div class="form-group">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="is_active" id="is_active-yes" value="true" required="required" @if (isset($country)) @if ($country->is_active == true) checked="checked" @endif @else checked="checked" @endif >
            <label class="form-check-label" for="is_active-yes">Yes</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" name="is_active" id="is_active-no" value="false" required="required" @if (isset($country) && $country->is_active == false) checked="checked" @endif >
            <label class="form-check-label" for="is_active-no">No</label>
          </div>
        </div>

        <div class="form-group">
          @if (isset($country))
            <a href="/admin/countries/{{ $country->slug }}/delete" class="btn btn-outline-danger float-right">Delete</a>
          @endif
            {!! Form::submit('Save',array('class'=>'btn btn-primary')) !!}

        </div>

    </div>
  </div>

  {!! Form::close() !!}


@endsection
