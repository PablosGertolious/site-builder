@extends('layouts.admin')

@section('content')

  <div class="row">
    <div class="col-12">
      <div class="page-header">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
          <li class="breadcrumb-item"><a href="/admin/blog/posts">Blog</a></li>
          <li class="breadcrumb-item"><a href="/admin/blog/categories">Categories</a></li>
          <li class="breadcrumb-item active">{{$blogPostCategory->name}}</li>
        </ol>

        <div class="float-right">
          <div class="btn-group" role="group">
            <a href="/admin/blog/categories" class="btn btn-secondary"><span class="fas fa-chevron-left"></span> Back</a>
            <a href="/admin/blog/categories/{{$blogPostCategory->slug}}/edit" class="btn btn-secondary"> Edit</a>
          </div>
        </div>

        <h1>{{$blogPostCategory->name}}</h1>
      </div>
    </div>
  </div>

  <!-- Display any alerts -->
  @include('components.alerts')
  <div class="row">
    @if($blogPostCategory->description!=null || $blogPostCategory->description!="")
      <div class="col-12 col-md-6">
        <p>{{$blogPostCategory->description}}</p>
      </div>
    @endif
    <div class="col-12 {{($blogPostCategory->description!=null || $blogPostCategory->description!=""?'col-md-6':'col-12')}}">
      <h3>Blog Posts</h3>
      <table  class="table table-sm table-striped">
        <thead class="thead-inverse">
          <tr>
            <th>Title</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          @if (count($postTitles) > 0)
            @foreach ($postTitles as $slug => $title)
              <tr>
                <td><a href="/admin/blog/posts/{{$slug}}" class="btn btn-sm btn-link">{{ $title ?? '' }}</a></td>
                <td class="text-right">
                  <div class="btn-group">
                    <a href="/admin/blog/posts/{{$slug}}" class="btn btn-primary btn-sm">
                      View
                    </a>
                    <button type="button" class="btn btn-sm btn-primary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                      <span class="sr-only">Toggle Dropdown</span>
                    </button>
                    <div class="dropdown-menu dropdown-menu-right">
                      <a href="/admin/blog/posts/{{ $slug }}/edit" class="dropdown-item">Edit</a>
                    </div>
                  </div>
                </td>
              </tr>
            @endforeach
          @else
            <tr>
              <td colspan="2" class="text-center">No blog posts found</td>
            </tr>
          @endif
        </tbody>
      </table>
    </div>
  </div>


@endsection
