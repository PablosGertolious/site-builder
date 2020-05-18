@extends('layouts.admin')

@section('content')

  <div class="row">
    <div class="col-12">
      <div class="page-header">
        <ol class="breadcrumb">
          <li class="breadcrumb-item"><a href="/admin">Home</a></li>
          <li class="breadcrumb-item active">Countries</li>
        </ol>

        <div class="float-right">
          <div class="btn-group" role="group">
            <a href="/admin/countries/create" class="btn btn-secondary"><i class="fas fa-plus" aria-hidden="true"></i> Add New</a>
          </div>
        </div>

        <h1>Countries <i class="fas fa-filter filter-toggle" aria-hidden="true" data-toggle="collapse" data-target="#filterCollapse" aria-expanded="false" aria-controls="filterCollapse"></i></h1>
      </div>
    </div>
  </div>

  <!-- Display any alerts -->
  @include('components.alerts')

  <div class="row">
    <div class="col-12">
      <div class="cardx bg-light mb-1 collapse @if ($hasFilter) show @endif" id="filterCollapse">
        <div class="card-body">
          <form action="/admin/countries" method="get" class="filters-form">
            <div class="row">
              <div class="col-12 col-md-3">
                <label class="sr-only" for="name">Name </label>
                <input type="text" class="form-control mr-1" id="name" name="name" placeholder="Name" value="@if (array_key_exists('name',$filters)){{ $filters['name'] }}@endif">
              </div>
              <div class="col-12 col-md-3">
                <button type="submit" class="btn btn-primary mr-1"><i class="fa fa-filter"></i></button>
                <a href="/admin/countries" class="btn btn-secondary"><i class="fa fa-times"></i></a>
                <input type="hidden" id="sort-column" name="sort-column" value="@if (array_key_exists('sort-column',$filters)){{ $filters['sort-column'] }}@else{{'name'}}@endif" />
                <input type="hidden" id="sort-order" name="sort-order" value="@if (array_key_exists('sort-order',$filters)){{ $filters['sort-order'] }}@else{{'asc'}}@endif" />
              </div>
            </div>

        </div>
      </div>
      <table class="table table-sm table-striped table-sortable">
        <thead class="thead-inverse">
          <tr>
            <th class="sortable-toggle" data-column="name">Name</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
@if (count($countries) > 0)
  @foreach ($countries as $country)
          <tr>
            <td><a href="/admin/countries/{{ $country->slug }}" class="btn btn-sm btn-link">{{ $country->name  }}</a></td>
            <td><a href="/admin/countries/{{ $country->slug }}" class="btn btn-sm btn-link">{{ $country->is_published ? 'Yes' : 'No' }}</a></td>
            <td class="text-right">
              <div class="btn-group">
                <a href="/admin/countries/{{ $country->slug }}" class="btn btn-primary btn-sm">
                  View
                </a>
                <button type="button" class="btn btn-sm btn-primary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <span class="sr-only">Toggle Dropdown</span>
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                  <a href="/admin/countries/{{ $country->slug }}/edit" class="dropdown-item">Edit</a>
                </div>
              </div>
            </td>
          </tr>
  @endforeach
@else
          <tr>
            <td colspan="3" class="text-center">No countries found. Why not <a href="/admin/countries/create">create the first one</a>?</td>
          </tr>
@endif
        </tbody>
      </table>
    </div>
  </div>

@endsection
