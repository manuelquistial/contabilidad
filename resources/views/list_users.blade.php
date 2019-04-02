@extends('layouts.app')

@section('lista_usuarios')
    <a class="nav-link active" href="{{ route('list_users') }}">{{ __('Lista Usuarios') }}</a>
@endsection

@section('content')
    @if (session('status'))
        <div class="alert alert-danger" role="alert">
            {{ session('status') }}
        </div>
    @endif
    <div class="row justify-content-center">
        <h2>Lista de Usuarios</h2>
        <table class="table">
            <thead>
                <tr>
                <th scope="col">{{ __('Nombre') }}</th>
                <th scope="col">{{ __('Usuario') }}</th>
                <th scope="col">{{ __('Email') }}</th>
                <th scope="col">{{ __('Role') }}</th>
                <th scope="col"></th>
                </tr>
            </thead>
            <tbody>
            @foreach ($users as $user)
                <tr>
                    <td>{{ $user->name }}</td>
                    <td>{{ $user->username }}</td>
                    <td>{{ $user->email }}</td>
                    <td>
                        @foreach ($user->roles as $role)
                            <a href="{{ route('user.rol', [$user->id]) }}" class="btn btn-link" onclick="return confirm('¿Esta seguro de cambiar rol?')">{{ $role->name }}</a>
                        @endforeach
                    </td>
                    <td>
                        <a href="{{ route('user.delete', [$user->id]) }}" class="btn btn-xs btn-danger" onclick="return confirm('¿Esta seguro de eliminar usuario?')">Delete</a>
                    </td>
                </tr>
            @endforeach
            </tbody>
        </table>
    </div>
@endsection
