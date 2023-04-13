$(document).ready(function(){
    $("input[name$='incidencias_mode']").click(function(){
        let test = $(this).val();
        if(test === "resumen"){
            $("p.detalle").addClass("ocultar");
        }
        else{
            $("p.detalle").removeClass("ocultar");
        }
    });
    $("input[name$='cc_mode']").click(function(){
        let test = $(this).val();
        if(test === "resumen"){
            $("p.detalle1").addClass("ocultar");
        }
        else{
            $("p.detalle1").removeClass("ocultar");
        }
    });
    $("input[name$='bcws_mode']").click(function(){
        let test = $(this).val();
        if(test === "original"){
            $("p.modificado").addClass("ocultar");
            $("p.orig-ev").removeClass("ocultar")
        }
        else{
            $("p.modificado").removeClass("ocultar")
            $("p.orig-ev").addClass("ocultar");
        }
    });
});

function toggleVis1(){
    let x = document.getElementById("hideShow");
    if(x.style.display === "none"){
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}

function toggleVis2(){
    let x = document.getElementById("hideShow2");
    if(x.style.display === "none"){
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}

function toggleVis3(){
    let x = document.getElementById("hideShow3");
    if(x.style.display === "none"){
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}

function toggleVis4(){
    let x = document.getElementById("hideShow4");
    if(x.style.display === "none"){
        x.style.display = "block";
    }
    else {
        x.style.display = "none";
    }
}

