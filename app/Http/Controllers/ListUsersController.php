<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\User;
use App\Role;
use Auth;

class ListUsersController extends Controller
{
    /**
     * Create a new controller instance.
     *
     * @return void
     */
    public function __construct(){
        $this->middleware('auth');
        $this->middleware(['role:administrador']);
    }

    public function index(){

        $users = User::all();

        return view('list_users', compact('users'));
    }

    public function update(Request $request, $id){

        $user = User::find($id);
        $userId = Auth::id();
        if($userId != $id){
            if($user->roles[0]['name'] == "administrador"){
                $user->roles()->detach(Role::where('name', "administrador")->first());
                $user->roles()->attach(Role::where('name', "usuario")->first());
            }else{
                $user->roles()->detach(Role::where('name', "usuario")->first());
                $user->roles()->attach(Role::where('name', "administrador")->first());
            }
            return redirect()->route('list_users');
        }else{
            $request->session()->flash('status', 'No puede cambiar su propio rol.');
            return redirect()->route('list_users');
        }
    }

    public function destroy(Request $request, $id) {

        $userId = Auth::id();
        if($userId != $id){
            $users = User::findOrFail($id);
            $users->delete();
            if($users->roles[0]['name'] == "administrador"){
                $users->roles()->detach(Role::where('name', "administrador")->first());
            }else{
                $users->roles()->detach(Role::where('name', "usuario")->first());
            }
        
            return redirect()->route('list_users');
        }else{
            $request->session()->flash('status', 'No puede eliminar su propio usuario.');
            return redirect()->route('list_users');
        }
    
    }
}
