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
                    background-color: #e9f3ff;
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

                .spinner {
                  width: 40px;
                  height: 40px;
                  background-color: #333;

                  margin: 30px auto;
                  -webkit-animation: sk-rotateplane 1.2s infinite ease-in-out;
                  animation: sk-rotateplane 1.2s infinite ease-in-out;
                }

                @-webkit-keyframes sk-rotateplane {
                  0% { -webkit-transform: perspective(120px) }
                  50% { -webkit-transform: perspective(120px) rotateY(180deg) }
                  100% { -webkit-transform: perspective(120px) rotateY(180deg)  rotateX(180deg) }
                }

                @keyframes sk-rotateplane {
                  0% {
                    transform: perspective(120px) rotateX(0deg) rotateY(0deg);
                    -webkit-transform: perspective(120px) rotateX(0deg) rotateY(0deg)
                  } 50% {
                    transform: perspective(120px) rotateX(-180.1deg) rotateY(0deg);
                    -webkit-transform: perspective(120px) rotateX(-180.1deg) rotateY(0deg)
                  } 100% {
                    transform: perspective(120px) rotateX(-180deg) rotateY(-179.9deg);
                    -webkit-transform: perspective(120px) rotateX(-180deg) rotateY(-179.9deg);
                  }
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
                  <div class="card-body" id="downloads">
                  </div>
                </div>
            </div>

            <input id="files" type="file" name="file" multiple hidden><br>
        </div>
    </body>

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
            dataUpload(document.getElementById("reservas").id);
        }, false);

        document.getElementById('conciliacion').addEventListener('click', function (evt) {
            dataUpload(document.getElementById("conciliacion").id);
        }, false);

        function dataUpload(url){
          let token = document.getElementsByTagName('meta')['csrf-token'].getAttribute("content");
          var num = document.getElementById("numero_centro").value;
          if(num != ""){
            _("downloads").style.display = "flex";
            let param = "num="+num;
            var ajax = new XMLHttpRequest();
            ajax.addEventListener("loadstart", function(event){
              _("downloads").innerHTML = '<div class="spinner"></div>';
            }, false);
            ajax.addEventListener("load", function(event){
              _("downloads").innerHTML = "";
              try{
                JSON.parse(event.target.responseText).forEach(function (file) {
                     _("downloads").innerHTML += '<div class="card"><div class="card-body"><h5 class="card-title">'+file.split('/').pop()+'</h5><a href="download?name='+file.split('/').pop()+'" role="button" class="btn btn-outline-danger">Descargar</a></div></div>'
                });
              }catch(e){
                _("downloads").style.display = "inline-flex";
                _("downloads").innerHTML = '<p id="downloads_text"></p>';
                if(JSON.parse(event.target.responseText).error == undefined){
                  _("downloads_text").innerHTML += JSON.parse(event.target.responseText).empty;
                  _("downloads_text").innerHTML += ", documentos encontrados:"
                  var value = JSON.parse(JSON.parse(event.target.responseText).files);
                  value.forEach(function (file) {
                       _("downloads_text").innerHTML += '<br>'+file.split('/').pop();
                  });
                }else{
                  _("downloads_text").innerHTML = JSON.parse(event.target.responseText).error;
                }
              }
            }, false);
            ajax.open("GET", "/"+url+"?"+param, true);
            ajax.setRequestHeader("X-CSRF-Token", token);
            ajax.send();
          }else{
            document.getElementById("numero_centro").style.backgroundColor = '#fb505f4d';
          }
        }

        document.getElementById('numero_centro').addEventListener('input', function (evt) {
          document.getElementById("numero_centro").style.backgroundColor = '#fff';
        }, false);
        /*document.addEventListener('click', function (evt) {
          if(evt.target.className.toString().includes("download")){
            let token = document.getElementsByTagName('meta')['csrf-token'].getAttribute("content");
            var name = "name="+evt.target.getAttribute("name");
            console.log(name)
            var ajax = new XMLHttpRequest();
            ajax.addEventListener("load", function(event){
              console.log(event.target.responseText)

            }, false);
            ajax.open("GET", "/download?"+name, true);
            ajax.setRequestHeader("X-CSRF-Token", token);
            ajax.send();
          }
        }, false);*/

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
            if(JSON.parse(event.target.responseText).success == undefined){
              _("status"+index).innerHTML = JSON.parse(event.target.responseText).error;
              _("status"+index).style.color = "#fb505f";
            }else{
              _("status"+index).innerHTML = JSON.parse(event.target.responseText).success;
              _("status"+index).style.color = "#4998db";
            }
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
