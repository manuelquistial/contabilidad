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
    let classes = document.getElementById('conciliacion');
    dataUpload(document.getElementById("reservas").id, classes);
}, false);

document.getElementById('conciliacion').addEventListener('click', function (evt) {
    let classes = document.getElementById('reservas');
    dataUpload(document.getElementById("conciliacion").id, classes);
}, false);

function dataUpload(url, classes){
    let token = document.getElementsByTagName('meta')['csrf-token'].getAttribute("content");
    var num = document.getElementById("numero_centro").value;
    if(num != ""){
        classes.classList.add('disabled');
        _("downloads").style.display = "flex";
        let param = "num="+num;
        var ajax = new XMLHttpRequest();
        ajax.addEventListener("loadstart", function(event){
            _("downloads").innerHTML = '<div class="spinner"></div>';
        }, false);
        ajax.addEventListener("load", function(event){
            _("downloads").innerHTML = "";
            let error = JSON.parse(event.target.responseText).error;
            let empty = JSON.parse(event.target.responseText).empty;
            if((error == undefined) & (empty == undefined)){
                JSON.parse(event.target.responseText).forEach(function (file) {
                    _("downloads").innerHTML += '<div class="card"><div class="card-body"><h5 class="card-title">'+file.split('/').pop()+'</h5><a href="'+window.location.href+'/download?name='+file.split('/').pop()+'" role="button" class="btn btn-outline-danger">Descargar</a></div></div>'
                });
                _("upload-boxes-file").innerHTML = '';
                classes.classList.remove('disabled');
            }else if(empty != undefined){
                classes.classList.remove('disabled');
                _("downloads").style.display = "inline-flex";
                _("downloads").innerHTML = '<p id="downloads_text"></p>';
                _("downloads_text").innerHTML += JSON.parse(event.target.responseText).empty;
                _("downloads_text").innerHTML += ", documentos encontrados:"
                var value = JSON.parse(JSON.parse(event.target.responseText).files);
                value.forEach(function (file) {
                    _("downloads_text").innerHTML += '<br>'+file.split('/').pop();
                });
            }else if(error != undefined){
                classes.classList.remove('disabled');
                _("downloads").style.display = "inline-flex";
                _("downloads").innerHTML = '<p id="downloads_text"></p>';
                _("downloads_text").innerHTML = error
            }
        }, false);
        ajax.open("GET", window.location.href+"/"+url+"?"+param, true);
        ajax.setRequestHeader("X-CSRF-Token", token);
        ajax.send();
    }else{
        document.getElementById("numero_centro").style.backgroundColor = '#fb505f4d';
    }
}

document.getElementById('numero_centro').addEventListener('input', function (evt) {
    document.getElementById("numero_centro").style.backgroundColor = '#fff';
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
        ajax.open("POST", window.location.href+"/file-upload", true);
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