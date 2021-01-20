function calculate() {
    var tmb = document.getElementById("tmb").value;
    var e = document.getElementById("mySelect");
    var strUser = e.options[e.selectedIndex].value;
    var resul = parseFloat(tmb) * strUser;

    document.getElementById("toret").value = resul;
    console.log(resul);


}

function caloriasDieta() {
    var calorias = document.getElementById('toret').value;
    var ajuste = document.getElementById('cantidad-ajuste').value;
    var e = document.getElementById('defsuperselect');
    var strUser = e.options[e.selectedIndex].value;
    var total;
    if (strUser == '1') {
        total = parseFloat(calorias) - parseFloat(ajuste);
    } else {
        total = parseFloat(calorias) + parseFloat(ajuste);
    }
    redondeo = Math.round(total);
    document.getElementById("calorias-dieta").value = redondeo
    document.getElementById("oculto").value = redondeo;
}

function Popup() {
    document.getElementById("popup-1").classList.toggle("active");
}

function Popup1() {
    document.getElementById("popup-2").classList.toggle("active");
}