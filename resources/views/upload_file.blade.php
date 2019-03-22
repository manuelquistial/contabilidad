@extends('layouts.app')

@section('style')
  <link href="{{ asset('css/style.css') }}" rel="stylesheet">
@endsection

@section('register')
@if (Route::has('register'))
    <a class="dropdown-item" href="{{ route('register') }}">{{ __('Registrar') }}</a>
@endif
@endsection

@section('content')
<div class="container">
    <div class="row upload"  style="margin-top: 20px;">
        <div class="row" style="width: 100%; justify-content: center;">
            <div>
                <input id="numero_centro" type="text" class="form-control" placeholder="Centro de Costo SAP">
            </div>
        </div>
        <div class="row" style="width: 60%;">
            <div class="col">
                <a role="button" class="btn btn-outline-primary" id="conciliacion">Conciliacion</a>
            </div>
            <div class="col">
                <a role="button" class="btn btn-outline-success" id="reservas" style="float: right;">Reservas</a>
            </div>
        </div>
        <div class="upload-boxes" id="upload-boxes-file"></div>
    </div>
    <div class="row upload">
        <div class="download-box text-center ">
          <div class="card-header">
              Documentos Generados
          </div>
          <div class="card-body" id="downloads">
          </div>
        </div>
    </div>

    <input id="files" type="file" name="file" multiple hidden><br>
</div>
@endsection
@section('script')
  <script src="{{ asset('js/script.js') }}" defer></script>
@endsection