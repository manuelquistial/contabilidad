<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{{ csrf_token() }}}">
        <title>Conciliacion - Facultad de Comunicaciones</title>
        <!-- Fonts -->
        <!-- Styles -->
        <style>
            body {
                font-family: 'PT Sans', sans-serif;
                width: 90%;
                max-width: 1050px;
                margin: 0 auto;
                color: #4e4242;
            }
            .upload-boxes{   
                break-inside: avoid;
                border-color: #c3dadc;
                border-radius: 8px 8px 8px 8px;
                border-style: dashed;
                margin: 10px;
                padding: 20px;
                page-break-inside: avoid;
                text-align: center;
                display: flex;
                flex-wrap: wrap;
                width: 60%;
                border-width: 2px;
            }
            .upload-boxes:hover{
                cursor:pointer;
            }

            .files-boxes{
                break-inside: avoid;
                border: 1px solid #bbbbbb;
                border-radius: 8px 8px 8px 8px;
                page-break-inside: avoid;
                margin: 10px;
                padding: 1em;
                width: 24%;
                text-align: center;
                display: flex;
                flex-direction: column;
            }

            .row{
                display: flex;
                justify-content: center;
                align-items: center;
            }

        </style>
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="upload-boxes" id="upload-boxes-file">
                </div>
            </div>
            <input id="files" type="file" name="file" multiple hidden><br>
        </div>
    </body>
    <script>
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
    
        function _(el) {
            return document.getElementById(el);
        }
        let index = 0
        function uploadFile(input, token) {
            const fileListAsArray = Array.from(input);
            fileListAsArray.forEach(function (file) {
                index += 1;
                var formdata = new FormData();
                formdata.append("file", file);
                var ajax = new XMLHttpRequest();
                _("upload-boxes-file").innerHTML += '<div class="files-boxes"><span>'+file.name+'</span><progress id="progressBar'+index+'" value="0" max="100" style="width: auto;"></progress><span id="status'+index+'"></span><span id="loaded_n_total'+index+'"></span></div>'
                ajax.upload.addEventListener("progress", function(evt){progressHandler(evt, index);}, false);
                ajax.addEventListener("load", function(evt){completeHandler(evt, index);}, false);
                ajax.addEventListener("error", function(evt){errorHandler(evt, index);}, false);
                ajax.addEventListener("abort", function(evt){abortHandler(evt, index);}, false);
                ajax.open("POST", "/file-upload", true);
                ajax.setRequestHeader("X-CSRF-Token", token);
                //ajax.send(formdata);
            });
            //alert(file.name+" | "+file.size+" | "+file.type);
            /*
            */
        }

        function progressHandler(event, index) {
        _("loaded_n_total"+index).innerHTML = "Uploaded " + event.loaded + " bytes of " + event.total;
        var percent = (event.loaded / event.total) * 100;
        _("progressBar"+index).value = Math.round(percent);
        _("status"+index).innerHTML = Math.round(percent) + "% uploaded... please wait";
        }

        function completeHandler(event, index) {
        _("status"+index).innerHTML = JSON.parse(event.target.responseText).success;
        _("progressBar"+index).value = 0; //wil clear progress bar after successful upload
        }

        function errorHandler(event, index) {
        _("status"+index).innerHTML = "Upload Failed";
        }

        function abortHandler(event, index) {
        _("status"+index).innerHTML = "Upload Aborted";
        }
    </script>
</html>
