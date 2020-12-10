document.querySelectorAll(".fileButton").forEach(inputElement => {
    const dropZoneElement = inputElement.closest(".fileContainer");

    inputElement.addEventListener("change", e =>{
        if(inputElement.files.length){
            updateThumbnail(dropZoneElement, inputElement.files[0]);
        }
    });

    dropZoneElement.addEventListener("dragover", e => {
        e.preventDefault();
        dropZoneElement.classList.add("fileContainer--over");
    });

    ["dragleave", "dragend"].forEach(type =>{
        dropZoneElement.addEventListener(type, e => {
            dropZoneElement.classList.remove("fileContainer--over");
        });
    });

    dropZoneElement.addEventListener("drop", e => {
        e.preventDefault();
        console.log(e.dataTransfer.files);

        if (e.dataTransfer.files.length){
            inputElement.files = e.dataTransfer.files;
            updateThumbnail(dropZoneElement, e.dataTransfer.files[0]);
        }

        dropZoneElement.classList.remove("fileContainer--over");
    });
});

var uploadForm = document.getElementById("uploadFileForm");

uploadForm.addEventListener("submit", (e) => {
    e.preventDefault();
    console.log("yay")
});

function updateThumbnail(dzElement, file){
    let thumbNailElement = dzElement.querySelector(".fileContainerThumb");

    if(dzElement.querySelector(".files")){
        dzElement.querySelector(".files").remove();
    }

    if(!thumbNailElement){
        thumbNailElement = document.createElement("div");
        thumbNailElement.classList.add("fileContainerThumb");
        dzElement.appendChild(thumbNailElement);
    }

    thumbNailElement.dataset.label = file.name;
    if(file.type.startsWith("image/")){
        const reader = new FileReader();

        reader.readAsDataURL(file);
        reader.onload = () =>{ 
            thumbNailElement.style.backgroundImage = `url('${reader.result}')`
        };
    }
    else{
        thumbNailElement.style.backgroundImage = null;
    }
}

function hideElement(){
    var before = document.getElementById("beforeUpload");
    var after = document.getElementById("afterUpload");
    before.style.display = "none";
    after.style.display = "block";
    // if(before.style.display === "none"){
    //     before.style.display = "block";
    // }
    // else {
    //     before.style.display = "none";
    // }
}
