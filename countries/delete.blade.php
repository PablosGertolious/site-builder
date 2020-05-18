@extends('layouts.admin')

@section('content')

  <div class="row">
    <div class="col-12 ">
      <div class="page-header">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
          <li class="breadcrumb-item"><a href="/admin/countries">Countries</a></li>
          <li class="breadcrumb-item"><a href="/admin/countries/{{$country->slug}}">{{$country->name}}</a></li>
          <li class="breadcrumb-item active">Delete</li>
        </ol>

        <div class="float-right">
          <div class="btn-group" role="group">
            <a href="/admin/countries/{{ $country->slug }}" class="btn btn-secondary"><i class="fas fa-chevron-left fa-fw" aria-hidden="true"></i> Back</a>
          </div>
        </div>

        <h1>Countries Delete</h1>
    </div>
    </div>
  </div>

  <!-- Display any alerts -->
  @include('components.alerts')

  <div class="row">
    <div class="col-12">
      {!! Form::model($country, array('url' => url('admin/countries/' .$country->slug . '/delete'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}
        <p>Are you sure you want to delete the Countries: <strong>{{ $country->name }}</strong>?</p>
        <p>Deletion is permanent and cannot be reversed.</p>

        <div class="form-group">
            {!! Form::submit('Yes, Delete',array('class'=>'btn btn-danger')) !!}
            <a href="/admin/countries/{{ $country->slug }}" class="btn btn-secondary">Cancel</a>
        </div>

      {!! Form::close() !!}

    </div>
  </div>

@endsection
