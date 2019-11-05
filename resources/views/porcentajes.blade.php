@extends('layouts.app')

@section('porcentajes')
    <a class="nav-link active" href="{{ route('list_porcentajes') }}">{{ __('Porcentajes') }}</a>
@endsection

@section('content')
    <div class="row justify-content-center">
        <div class="col-md-8">
            @if (session('status'))
                <div class="alert alert-success" role="alert">
                    {{ session('status') }}
                </div>
            @endif
            <div class="card">
                <div class="card-header">{{ __('Porcentajes') }}</div>
                <div class="card-body">
                    <form method="GET" action="{{ route('update_porcentajes', [$porcentajes[0]->id]) }}">
                        {!! csrf_field() !!}
                        <div class="form-group row">
                            <label for="porcentaje_salud" class="col-md-4 col-form-label text-md-right">{{ __('Salud') }}</label>

                            <div class="col-md-6">
                                <input id="porcentaje_salud" type="text" class="form-control{{ $errors->has('porcentaje_salud') ? ' is-invalid' : '' }}" name="porcentaje_salud" value="{{ $porcentajes[0]->porcentaje_salud }}" required>

                                @if ($errors->has('porcentaje_salud'))
                                    <span class="invalid-feedback">
                                        <strong>{{ $errors->first('porcentaje_salud') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>
                        <div class="form-group row">
                            <label for="porcentaje_ingresos" class="col-md-4 col-form-label text-md-right">{{ __('Ingresos') }}</label>

                            <div class="col-md-6">
                                <input id="porcentaje_ingresos" type="text" class="form-control{{ $errors->has('porcentaje_ingresos') ? ' is-invalid' : '' }}" name="porcentaje_ingresos" value="{{ $porcentajes[0]->porcentaje_ingresos }}" required>

                                @if ($errors->has('porcentaje_ingresos'))
                                    <span class="invalid-feedback" role="alert">
                                        <strong>{{ $errors->first('porcentaje_ingresos') }}</strong>
                                    </span>
                                @endif
                            </div>
                        </div>

                        <div class="form-group row mb-0">
                            <div class="col-md-6 offset-md-4">
                                <button type="submit" class="btn btn-primary">
                                    {{ __('Actualizar') }}
                                </button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
@endsection
