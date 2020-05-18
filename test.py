name = "$cou_ntr_ies".replace("_"," ")
string = f"@extends('layouts.admin')@s\"ection('content')  @if (isset({name.capitalize()}))    {{!! Form::model({name}, array('url' => url('admin/categories/' .{name}->slug . '/edit'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}}}}  @else    {{!! Form::open(array('url' => url('admin/categories/create'), 'method' => 'post', 'class' => 'form', 'files'=> false)) !!}}}}  @endif"
print(string)
