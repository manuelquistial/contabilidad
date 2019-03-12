<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;


class UploadFileController extends Controller
{
    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */

    public function index(){
        return view('upload_file');
    }

    public function downloadReservas(){
        $data = glob(public_path('files').'/files_out/*');
        return json_encode($data);
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */
    public function downloadConciliacion(Request $request)
    {
        $request->validate([
            'num' => 'required',
        ]);

        $value = request()->num;
        $files = glob(public_path('files/conciliacion')."/*.{xlsx,XLSX}", GLOB_BRACE);
        //echo $files;
        $param = exec("python3 ".public_path()."/files/conciliacion.py ".$value." ".$files[0]." ".$files[1]." ".$files[2]." ".public_path('files/'));
        if($param){
          $data = glob(public_path('files').'/files_out/*');
          return json_encode($data);
        }else{
          return response()->json(['success'=>'Error en la descarga, comuniquese con soporte']);
        }
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */
    public function fileUploadPost(Request $request)
    {
        $request->validate([
            'file' => 'required',
		     ]);

        $fileName = request()->file->getClientOriginalName();
        if(strpos(strtolower($fileName), "reservas") !== false){
          request()->file->move(public_path('files/reservas'), $fileName);
        }else{
          request()->file->move(public_path('files/conciliacion'), $fileName);
        }

        return response()->json(['success'=>'Archivo agregado']);
    }
}
