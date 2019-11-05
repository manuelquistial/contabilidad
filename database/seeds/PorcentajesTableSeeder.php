<?php

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class PorcentajesTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        DB::table('porcentajes')->insert([
            'porcentaje_salud' => '0.24023',
            'porcentaje_ingresos' => '0.6667'
        ]);
    }
}
