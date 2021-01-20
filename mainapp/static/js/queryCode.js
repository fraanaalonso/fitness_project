$("document").ready(function() {

    $("#tmb-in").on("click", function() {

        $("#formBox").fadeIn("fast", function() {
            $("#button-calorie").fadeIn("fast", function() {
                $("#normo-in").on("click", function() {
                    $("#final-result").fadeIn("fast");
                });
            });
        });
    });

    $("#tmb-out").on("click", function() {
        $("#final-calc").fadeOut("fast");
        $("#final-result").fadeOut("fast");
        $("#div-opcion").fadeOut("fast");
        $("#formBox").fadeOut("fast", function() {
            $("#button-calorie").fadeOut("fast", function() {
                $("#final-result").fadeOut("fast");
                $("#normo-out").on("click", function() {
                    $("#final-calc").fadeOut("fast");
                    $("#final-result").fadeOut("fast");
                    $("#div-opcion").fadeOut("fast");
                });
            });
        });
    });


});


$("document").ready(function() {
    $("#ajuste-in").on("click", function() {
        $("#div-opcion").fadeIn("fast", function() {
            $("#mostrar-calorias").on("click", function() {
                $("#final-calc").fadeIn("fast");
            });
        });
    });

    $("#ajuste-out").on("click", function() {
        $("#div-opcion").fadeOut("fast", function() {
            $("#final-calc").fadeOut("fast");
            $("#div-opcion").fadeOut("fast");
            $("#mostrar-calorias-out").on("click", function() {
                $("#final-calc").fadeOut("fast");
            });
        });
    });
});


$("document").ready(function() {
    $("#button-calcular-distribución").on("click", function() {
        $("distribucion-macros").fadeIn("fast");
    })
})



$("document").ready(function() {
    $("#normo-in").on("click", function() {
        $("#mySelect").attr('disabled', 'disabled');
    });
    $("#normo-out").on("click", function() {
        $("#mySelect").prop('disabled', false);
        $("#cantidad-ajuste").prop('disabled', false);
        $("#defsuperselect").prop('disabled', false);
    });
    $("#tmb-out").on("click", function() {
        $("#mySelect").prop('disabled', false);
        $("#cantidad-ajuste").prop('disabled', false);
        $("#defsuperselect").prop('disabled', false);
    });

    $("#ajuste-in").on("click", function() {
        $("#cantidad-ajuste").attr('disabled', 'disabled');
    });
    $("#ajuste-out").on("click", function() {
        $("#cantidad-ajuste").prop('disabled', false);
        $("#defsuperselect").prop('disabled', false);
    });

    $("#mostrar-calorias").on("click", function() {
        $("#defsuperselect").attr('disabled', 'disabled');
    });
    $("#mostrar-calorias-out").on("click", function() {
        $("#defsuperselect").prop('disabled', false);
    });

});



$("#document").ready(function() {
    $("#hide-info-button").on("click", function() {
        $("#show-info").fadeOut("fast");
        $("#div-button-in").fadeIn("fast");
    });
});

$("#document").ready(function() {
    $("#show-info-button").on("click", function() {
        $("#div-button-in").fadeOut("fast");
        $("#show-info").fadeIn("fast");
    });
});