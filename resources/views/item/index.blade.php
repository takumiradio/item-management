@extends('adminlte::page')

@section('title', '商品一覧')

@section('content_header')
    <h1>トミカ一覧</h1>
@stop

@section('content')
    <div class="row">
        <div class="col-12">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">トミカ一覧</h3>
                    <div class="card-tools">
                        <div class="input-group input-group-sm">
                            <div class="input-group-append">
                                <a href="{{ url('items/add') }}" class="btn btn-default">トミカ登録</a>                                
                            </div>
                        </div>
                    </div>
                </div>
                
            </div>
            <div class="d-flex flex-wrap">
            @foreach($items as $item) 
                        <div class="card mr-2" style="width: 18rem;">
                            <img src="data:image/png;base64,{{$item->image}}" class="card-img-top" alt="...">
                            <div class="card-body">
                                <h5 class="card-title">{{$item->name}}</h5>
                                <p class="card-text">{{$item->detail}}</p>
                                <div class="d-flex flex-wrap">
                                    <a href="{{ url('items/edit/'.$item->id)}}" class="btn btn-primary mr-2">編集</a>
                                    <form action="{{ url('items/delete') }}" method="POST"
                                        onsubmit = "return confirm('削除します。よろしいですか？');">
                                        @csrf
                                        <input type="hidden" name="id" value="{{ $item->id }}">
                                        <input type="submit" value="削除" class="btn btn-danger">
                                    </form>
                                </div>
                            </div>
                        </div>
            @endforeach
            </div>
        </div>
    </div>
@stop

@section('css')
@stop

@section('js')
@stop
