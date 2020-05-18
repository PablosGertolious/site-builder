@extends('layouts.admin')

@section('content')

  <div class="row">
    <div class="col-12">
      <div class="page-header">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
          <li class="breadcrumb-item"><a href="/admin/posts">Blog</a></li>
          <li class="breadcrumb-item"><a href="/admin/countries">Countries</a></li>
          <li class="breadcrumb-item active">{{$country->name}}</li>
        </ol>

        <div class="float-right">
          <div class="btn-group" role="group">
            <a href="/admin/countries" class="btn btn-secondary"><span class="fas fa-chevron-left"></span> Back</a>
            <a href="/admin/countries/{{$country->slug}}/edit" class="btn btn-secondary"> Edit</a>
          </div>
        </div>

        <h1>{{$country->name}}</h1>
      </div>
    </div>
  </div>

  <!-- Display any alerts -->
  @include('components.alerts')



@endsection
