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
    public function fileUploadPost(Request $request)
    {
        $request->validate([
            'file' => 'required',
		]);
 
        $fileName = request()->file->getClientOriginalName();
        
        request()->file->move(public_path('files'), $fileName);
 
        return response()->json(['success'=>'You have successfully upload file.']);
    }
}