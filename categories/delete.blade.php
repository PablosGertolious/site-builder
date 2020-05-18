@extends('layouts.admin')

@section('content')

  <div class="row">
    <div class="col-12 ">
      <div class="page-header">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
          <li class="breadcrumb-item"><a href="/admin/blog/posts">Blog</a></li>
          <li class="breadcrumb-item"><a href="/admin/blog/categories">Categories</a></li>
          <li class="breadcrumb-item"><a href="/admin/blog/categories/{{$blogPostCategory->slug}}">{{$blogPostCategory->name}}</a></li>
          <li class="breadcrumb-item active">Delete</li>
        </ol>

        <div class="float-right">
          <div class="btn-group" role="group">
            <a href="/admin/blog/categories/{{ $blogPostCategory->slug }}" class="btn btn-secondary"><i class="fas fa-chevron-left fa-fw" aria-hidden="true"></i> Back</a>
          </div>
        </div>

        <h1>Blog Post Category Delete</h1>
    </div>
    </div>
  </div>

  <!-- Display any alerts -->
  @include('components.alerts')

  <div class="row">
    <div class="col-12">
      {!! Form::model($blogPostCategory, array('url' => url('admin/blog/categories/' .$blogPostCategory->slug . '/delete'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}
        <p>Are you sure you want to delete the Blog Post Category: <strong>{{ $blogPostCategory->name }}</strong>?</p>
        <p>Deletion is permanent and cannot be reversed.</p>

        <div class="form-group">
            {!! Form::submit('Yes, Delete',array('class'=>'btn btn-danger')) !!}
            <a href="/admin/blog/categories/{{ $blogPostCategory->slug }}" class="btn btn-secondary">Cancel</a>
        </div>

      {!! Form::close() !!}

    </div>
  </div>

@endsection
