<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{{ csrf_token() }}}">
        <title>Conciliacion - Facultad de Comunicaciones</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">
            <style>
                .upload-boxes{
                    border-color: #c3dadc;
                    border-radius: 8px 8px 8px 8px;
                    border-style: dashed;
                    margin: 10px;
                    padding: 20px;
                    page-break-inside: avoid;
                    text-align: center;
                    display: flex;
                    flex-wrap: wrap;
                    width: 78%;
                    border-width: 2px;
                    min-height: 150px;
                }

                .upload-boxes:hover{
                    cursor: pointer;
                    border: 2px dashed green;
                }

                .download-box{
                    border-color: #c3dadc;
                    border-radius: 8px 8px 8px 8px;
                    border-style: dashed;
                    margin: 10px;
                    page-break-inside: avoid;
                    width: 78%;
                    border-width: 2px;
                }

                .files-boxes{
                    break-inside: avoid;
                    border: 1px solid #bbbbbb;
                    border-radius: 8px 8px 8px 8px;
                    page-break-inside: avoid;
                    margin: 10px;
                    padding: 1em;
                    width: 30%;
                    text-align: center;
                    display: flex;
                    flex-direction: column;
                }

                .upload{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }

                .row{
                    margin: 5px 0 5px;
                }

                .card{
                    width: 16rem;
                    margin: 8px;
                }

                #downloads {
                    display: flex;
                }

            </style>

    </head>
    <body>
        <div class="container">
        <nav class="navbar navbar-light bg-light">
            <a class="navbar-brand">Conciliacion - Facultad de Comunicaciones</a>
        </nav>
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
                <div class="card-body" id="downloads"></div>
                </div>
            </div>

            <input id="files" type="file" name="file" multiple hidden><br>
        </div>
    </body>
        <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

    <script type="text/javascript">

        var inputFile = document.getElementById("files");

        document.body.addEventListener('dragover', function (evt) {
            evt.stopPropagation();
            evt.preventDefault();
            evt.dataTransfer.dropEffect = 'copy';
        }, false);

        document.body.addEventListener('drop', function (evt) {
            evt.stopPropagation();
            evt.preventDefault();
            if (evt.target.className === 'upload-boxes') {
                evt.target.style.border = "";
                let meta = document.getElementsByTagName('meta')['csrf-token'].getAttribute("content");
                let files = evt.target.files || evt.dataTransfer.files;
                uploadFile(files, meta);
            }
        }, false);

        document.body.addEventListener('click', function (evt) {
            if (evt.target.className === 'upload-boxes') {
                inputFile.click();
            }
        }, false);

        document.getElementById('files').addEventListener('change', function (evt) {
            let meta = document.getElementsByTagName('meta')['csrf-token'].getAttribute("content");
            let files = evt.target.files || evt.dataTransfer.files;
            uploadFile(files, meta);
        }, false);

        document.body.addEventListener('dragenter', function (evt) {
            if (evt.target.className === 'upload-boxes') {
                evt.target.style.border = "2px dashed green";
            }
        }, false);

        document.body.addEventListener('dragleave', function (evt) {
            if (evt.target.className === 'upload-boxes') {
                evt.target.style.border = "";
            }
        }, false);

        document.getElementById('reservas').addEventListener('click', function (evt) {
            _("downloads").innerHTML = "";
            let token = document.getElementsByTagName('meta')['csrf-token'].getAttribute("content");
            var num = document.getElementById("numero_centro").value;
            if(num != ""){
              let param = "num="+num;
              var ajax = new XMLHttpRequest();
              ajax.addEventListener("load", function(event){
                try{
                  JSON.parse(event.target.responseText).forEach(function (file) {
                       _("downloads").innerHTML += '<div class="card"><div class="card-body"><h5 class="card-title">'+file.split('/').pop()+'</h5><a role="button" class="btn btn-outline-danger">Descargar</a></div></div>'
                  });
                }catch(e){
                  _("downloads").innerHTML = JSON.parse(event.target.responseText).sucess;
                }
              }, false);
              ajax.open("GET", "/reservas?"+param, true);
              ajax.setRequestHeader("X-CSRF-Token", token);
              ajax.send();
            }else{

            }
        }, false);

        document.getElementById('conciliacion').addEventListener('click', function (evt) {
            _("downloads").innerHTML = "";
            let token = document.getElementsByTagName('meta')['csrf-token'].getAttribute("content");
            var num = document.getElementById("numero_centro").value;
            let param = "num="+num;
            var ajax = new XMLHttpRequest();
            ajax.addEventListener("load", function(event){
              try{
                JSON.parse(event.target.responseText).forEach(function (file) {
                     _("downloads").innerHTML += '<div class="card"><div class="card-body"><h5 class="card-title">'+file.split('/').pop()+'</h5><a role="button" class="btn btn-outline-danger">Descargar</a></div></div>'
                });
              }catch(e){
                _("downloads").innerHTML = JSON.parse(event.target.responseText).success;
              }
            }, false);
            ajax.open("GET", "/conciliacion?"+param, true);
            ajax.setRequestHeader("X-CSRF-Token", token);
            ajax.send();
        }, false);

        function uploadFile(input, token){
            const fileListAsArray = Array.from(input);
            fileListAsArray.forEach(function (file, index) {
                var formdata = new FormData();
                formdata.append("file", file);
                var ajax = new XMLHttpRequest();
                _("upload-boxes-file").innerHTML += '<div class="files-boxes"><span>'+file.name+'</span><progress id="progressBar'+index+'" value="0" max="100" style="width: auto;"></progress><span id="status'+index+'"></span></div>'
                ajax.upload.addEventListener("progress", function(evt){
                    progressHandler(evt, index);}, false);
                ajax.addEventListener("load", function(evt){
                    completeHandler(evt, index);}, false);
                ajax.addEventListener("error", function(evt){errorHandler(evt, index);}, false);
                ajax.addEventListener("abort", function(evt){abortHandler(evt, index);}, false);
                ajax.open("POST", "/file-upload", true);
                ajax.setRequestHeader("X-CSRF-Token", token);
                ajax.send(formdata);
            });
            //alert(file.name+" | "+file.size+" | "+file.type);
            /*
            */
        }
        function _(el) {
            return document.getElementById(el);
        }

        function progressHandler(event, index) {
            //<span id="loaded_n_total'+index+'"></span>
            //_("loaded_n_total"+index).innerHTML = "Uploaded " + event.loaded + " bytes of " + event.total;
            var percent = (event.loaded / event.total) * 100;
            _("progressBar"+index).value = Math.round(percent);
            _("status"+index).innerHTML = Math.round(percent) + "% uploaded... please wait";
        }

        function completeHandler(event, index) {
            _("status"+index).innerHTML = JSON.parse(event.target.responseText).success;
            _("progressBar"+index).value = 0; //wil clear progress bar after successful upload
            //_("loaded_n_total"+index).removeAttribute("id");
            _("status"+index).removeAttribute("id");
            _("progressBar"+index).removeAttribute("id");
        }

        function errorHandler(event, index) {
        _("status"+index).innerHTML = "Upload Failed";
        }

        function abortHandler(event, index) {
        _("status"+index).innerHTML = "Upload Aborted";
        }
    </script>
</html>
