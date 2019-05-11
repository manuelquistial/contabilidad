<?php

namespace App\Http\Controllers;
use Auth;
use Illuminate\Http\Request;
use File;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class UploadFileController extends Controller
{
    public function __construct(){
        $this->middleware('auth');
    }
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
      $userId = Auth::id();
      $value = request()->num;
      $files = glob(storage_path('app/public/files/reservas')."/*".$value."_".$userId.".{xlsx,XLSX}", GLOB_BRACE);
      if(empty($files) || (count($files) != 2)){
        return response()->json(['empty'=>'No existen los documentos necesarios para realizar reservas', 'files'=>json_encode($files)]);
      }else{
        $param = new Process("python3 ".storage_path('app/public')."/reservas.py ".$value." ".$files[0]." ".$files[1]." ".storage_path('app/public/files/')." ".$userId);
        $param->run();
        if (!$param->isSuccessful()) {
          throw new ProcessFailedException($param);
          return response()->json(['error'=>'Error en la ejecucion del programa de reservas.']);
        }else{
          FILE::delete($files);
          $data = glob(storage_path('app/public/files/').'files_out/*'.$value."_".$userId.'.xlsx');
          return json_encode($data);
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
        $userId = Auth::id();
        $value = request()->num;
        $files = glob(storage_path('app/public/files/conciliacion')."/*".$value."_".$userId.".{xlsx,XLSX}", GLOB_BRACE);
        if(empty($files) || (count($files) != 3)){
          return response()->json(['empty'=>'No existen los documentos necesarios para conciliar', 'files'=>json_encode($files)]);
        }else{
          $param = new Process("python3 ".storage_path('app/public')."/conciliacion.py ".$value." ".$files[0]." ".$files[1]." ".$files[2]." ".storage_path('app/public/files/')." ".$userId);
          $param->run();
          if (!$param->isSuccessful()) {
            throw new ProcessFailedException($param);
            return response()->json(['error'=>'Error en la ejecucion del programa de conciliacion.']);
          }else{
            FILE::delete($files);
            $data = glob(storage_path('app/public/files/').'files_out/*'.$value."_".$userId.'.xlsx');
            return json_encode($data);
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
        $userId = Auth::id();
        $request->validate([
            'name' => 'required',
        ]);
        $name = request()->name;
        $file = storage_path('app/public/files/files_out/').$name;
        $name = explode("_", request()->name);
        array_pop($name);
        return response()->download($file, implode("_", $name).".xlsx")->deleteFileAfterSend(true);
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
         
        $userId = Auth::id();
        $fileName = strtolower(request()->file->getClientOriginalName());
        $fileName = str_replace(".xlsx","",$fileName);
        $fileName = $fileName."_".$userId.".xlsx";
        $var = strtolower($fileName);
        if((strpos($var, "reservas") !== false) & ((strpos($var, "sap") !== false) || (strpos($var, "sigep") !== false))){
          request()->file->move(storage_path('app/public/files/reservas'), $fileName);
          return response()->json(['success'=>'Archivo agregado']);
        }elseif((strpos($var, "pagos") !== false) || (strpos($var, "recaudos") !== false) || (strpos($var, "general") !== false)){
          request()->file->move(storage_path('app/public/files/conciliacion'), $fileName);
          return response()->json(['success'=>'Archivo agregado']);
        }else{
          return response()->json(['error'=>'Archivo incorrecto']);
        }
    }
}
