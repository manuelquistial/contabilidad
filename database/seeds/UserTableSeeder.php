<?php

use Illuminate\Database\Seeder;
use App\User;
use App\Role;

class UserTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $role_administrador = Role::where('name', 'administrador')->first();
        $user = new User();
        $user->name = 'prueba';
        $user->username = 'prueba';
        $user->email = 'prueba@udea.edu.co';
        $user->password = bcrypt(1234);
        $user->token = '';
        $user->save();
        $user->roles()->attach($role_administrador);
    }
}
