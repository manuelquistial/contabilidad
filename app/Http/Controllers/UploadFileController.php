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

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */
    public function downloadReservas(Request $request){
      $request->validate([
          'num' => 'required',
      ]);

      $value = request()->num;
      $files = glob(public_path('files/reservas')."/*.{xlsx,XLSX}", GLOB_BRACE);
      if(empty($files) || (count($files) != 2)){
        return response()->json(['empty'=>'No existen los documentos necesarios para realizar reservas', 'files'=>json_encode($files)]);
      }else{
        $param = exec("python3 ".public_path()."/files/reservas.py ".$value." ".$files[0]." ".$files[1]." ".public_path('files/'));
        if($param){
          $data = glob(public_path('files').'/files_out/*');
          return json_encode($data);
        }else{
          return response()->json(['error'=>'Error en la descarga, comuniquese con soporte']);
        }
      }
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
        if(empty($files) || (count($files) != 3)){
          return response()->json(['empty'=>'No existen los documentos necesarios para conciliar', 'files'=>json_encode($files)]);
        }else{
          $param = exec("python3 ".public_path()."/files/conciliacion.py ".$value." ".$files[0]." ".$files[1]." ".$files[2]." ".public_path('files/'));
          if($param){
            $data = glob(public_path('files').'/files_out/*');
            return json_encode($data);
          }else{
            return response()->json(['error'=>'Error en la descarga, comuniquese con soporte']);
          }
        }
    }

    /**
     * Show the application dashboard.
     *
     * @return \Illuminate\Http\Response
     */
    public function download(Request $request)
    {
        $request->validate([
            'name' => 'required',
        ]);
        $name = request()->name;
        $file = public_path('files/files_out/').$name;
        return response()->download($file, $name)->deleteFileAfterSend(true);
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
        $var = strtolower($fileName);
        if(strpos($var, "reservas") !== false){
          request()->file->move(public_path('files/reservas'), $fileName);
          return response()->json(['success'=>'Archivo agregado']);
        }elseif((strpos($var, "pagos") !== false) || (strpos($var, "recaudos") !== false) || (strpos($var, "general") !== false)){
          request()->file->move(public_path('files/conciliacion'), $fileName);
          return response()->json(['success'=>'Archivo agregado']);
        }else{
          return response()->json(['error'=>'Archivo incorrecto']);
        }
    }
}
