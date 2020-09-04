var pago_cancelado = 0
var ph = 0
var ec = 0
var temperatura = 0
var nivel = 0
var url = "ws://192.168.0.100:8000"
var myChart = new FusionCharts({
    type: 'realtimelinedy',
    dataFormat: 'json',
    id: 'stockMonitor',
    renderAt: 'chart-container',
    width: '1600',
    height: '550',
    dataSource: {
        "chart": {
            "theme": "fusion",
            "caption": "Monitor del agua",
            "subCaption": "Hidroponia",
            "captionFontSize": "14",
            "subcaptionFontSize": "14",
            "baseFontColor": "#333333",
            "baseFont": "Helvetica Neue,Arial",
            "subcaptionFontBold": "0",
            "paletteColors": "#0075c2,#1aaf5d,#f2c500",
            "bgColor": "#ffffff",
            "canvasBgColor": "#ffffff",
            "showBorder": "0",
            "showShadow": "0",
            "showCanvasBorder": "0",
            "showRealTimeValue": "0",
            "legendBorderAlpha": "0",
            "legendShadow": "0",
            "numberprefix": "",
            "setadaptiveymin": "1",
            "setadaptivesymin": "1",
            "xaxisname": "Hora",
            "labeldisplay": "Rotate",
            "slantlabels": "1",
            //"pyaxisminvalue": "35",
            //"pyaxismaxvalue": "36",
            //"syaxisminvalue": "4",
            //"syaxismaxvalue": "50",
            "divlineAlpha": "100",
            "divlineColor": "#999999",
            "showAlternateHGridColor": "0",
            "divlineThickness": "1",
            "divLineIsDashed": "1",
            "divLineDashLen": "1",
            "divLineGapLen": "1",
            "numDisplaySets": "1500"
        },
        "categories": [{
            "category": [{
                "label": "Day Start"
            }]
        }],
        "dataset": [{
                "seriesname": "PH",
                "showvalues": "0",
                "data": [{
                    "value": "0"
                }]
            },
            {
                "seriesname": "EC",
                "showvalues": "0",
                "parentyaxis": "E",
                "data": [{
                    "value": "0"
                }]
            },
            {
                "seriesname": "Temperatura",
                "showvalues": "0",
                "parentyaxis": "T",
                "data": [{
                    "value": "0"
                }]
            },
            {
                "seriesname": "Nivel",
                "showvalues": "0",
                "parentyaxis": "N",
                "data": [{
                    "value": "0"
                }]
            }
        ],
        "trendlines": [{
            "line": [{
                    "parentyaxis": "P",
                    "startvalue": "0",
                    "displayvalue": "Open",
                    "thickness": "1",
                    "color": "red",
                    "dashed": "1"
                },
                {
                    "parentyaxis": "E",
                    "startvalue": "0",
                    "displayvalue": "Open",
                    "thickness": "1",
                    "color": "#1aaf5d",
                    "dashed": "1"
                },
                {
                    "parentyaxis": "T",
                    "startvalue": "0",
                    "displayvalue": "Open",
                    "thickness": "1",
                    "color": "#ffffff",
                    "dashed": "1"
                },
                {
                    "parentyaxis": "N",
                    "startvalue": "0",
                    "displayvalue": "Open",
                    "thickness": "1",
                    "color": "#1aaf5d",
                    "dashed": "1"
                }

            ]
        }]
    },
    "events": {
        "initialized": function(e) {
            function formatTime(num) {
                return (num <= 9) ? ("0" + num) : num;
            }

            function updateData() {
                // Get reference to the chart using its ID
                var chartRef = FusionCharts("stockMonitor"),
                    //We need to create a querystring format incremental update, containing
                    //label in hh:mm:ss format
                    //and a value (random).
                    currDate = new Date(),
                    label = formatTime(currDate.getHours()) + ":" + formatTime(currDate.getMinutes()) + ":" + formatTime(currDate.getSeconds()),
                    //Get random number between 35.25 & 30.75 - rounded to 2 decimal places
                    //hrys = Math.floor(Math.random() *
                    //    50) / 100 + 35.25,

                    //Get random number between 10962.87 & 11052.87

                    //Build Data String in format &label=...&value=...
                    strData = "&label=" + label + "&value=" + ph + "|" + ec + "|" + temperatura + "|" + nivel;
                //Feed it to chart.
                chartRef.feedData(strData);
                console.log(ph);
            }
            var myVar = setInterval(function() {
                updateData();
            }, 20000);
        }
    }
}).render();


$(document).ready(function() {

    var socket = new WebSocket(url);
    socket.onopen = websocket_conexion_ok;
    socket.onmessage = websocket_msj_recibido;


});

function opcionPresionada(opcion) {
    var op1 = $("input[type=checkbox][name=op1]:checked").val()
    var op2 = $("input[type=checkbox][name=op2]:checked").val()
    var op3 = $("input[type=checkbox][name=op3]:checked").val()
    if (opcion == 1) {
        deshabilitar_opciones();
        habilitar_opcion("#op1")
    } else if (opcion == 2) {
        deshabilitar_opciones();
        habilitar_opcion("#op2")
    } else if (opcion == 3) {
        deshabilitar_opciones();
        habilitar_opcion("#op3")
    }



    // $('#cobro').trigger('click');
    // $('#recarga').trigger('click');
    $('[href="#recarga"]').tab('show');
    // console.log("fin");
}

function habilitar_opcion(opcion) {
    console.log("opcion:...", opcion);
    $(opcion).prop("checked", true);
}

function deshabilitar_opciones(num) {
    $("#op1").prop("checked", false);
    $("#op2").prop("checked", false);
    $("#op3").prop("checked", false);
}

function aler() {
    pago_cancelado = 1
    alert(pago_cancelado);
}

function enviar_respuesta() {
    console.log(pago_cancelado)
}

function websocket_conexion_ok() {
    //alert();

}

function websocket_msj_recibido(e) {
    console.log(myChart.originalDataSource.dataset[0].data[0].value);
    datos = JSON.parse(e.data);
    //alert('mensaje recibido' + datos.fecha);
    enviar_respuesta()
    $('#contador').text(datos.monto)
    if (datos.fecha == undefined) { datos.fecha = "-" }
    if (datos.monto_ingresar == undefined) { datos.monto_ingresar = "-" }
    if (datos.monto_ingresado == undefined | datos.monto_ingresado == 0) { datos.monto_ingresado = "--" }
    if (datos.monto_a_dispensar == undefined) { datos.monto_a_dispensar = "-" }
    if (datos.folio == undefined) { datos.folio = "-" }
    if (datos.hora_entrada == undefined) { datos.hora_entrada = "-" }
    if (datos.tiempo_estacionado == undefined) { datos.tiempo_estacionado = "-" }
    if (datos.descuento == undefined) { datos.descuento = "--" }

    if (datos.X_17 == undefined) { datos.X_17 = "-" } else { datos.X_17 = "$" + datos.X_17 + ".00" }
    if (datos.X_20 == undefined) { datos.X_20 = "-" } else { datos.X_20 = "$" + datos.X_20 + ".00" }

    if (datos.ph == undefined) { datos.ph = "-" } else { datos.ph = datos.ph }
    if (datos.ec == undefined) { datos.ec = "-" } else { datos.ec = datos.ec }
    if (datos.nivel == undefined) { datos.nivel = "-" } else { datos.nivel = datos.nivel }
    if (datos.temperatura == undefined) { datos.temperatura = "-" } else { datos.temperatura = datos.temperatura + "°C" }

    //myChart.originalDataSource.dataset[0].data[0].value = 38.23
    //myChart.updateData(10)
    ph = datos.ph
    ec = datos.ec
    temperatura = datos.temperatura
    nivel = datos.nivel
    $('#sensor-ph').text(datos.ph)
    $('#sensor-ec').text(datos.ec)
    $('#sensor-temperatura').text(datos.temperatura)
    $('#sensor-nivel').text(datos.nivel)
    $('#fecha').text(datos.fecha)
    $('#progreso').text(" Progreso del tratamiento: " + datos.nivel_completado + "  %")




    $('.date').text(datos.fecha)
    $('.total-td').text(datos.X_17)
    $('.ingresado-td').text(datos.X_20)

    $('#monto_ingresar').text(datos.monto_ingresar)
    $('#monto_ingresado').text(datos.monto_ingresado)
    $('#monto_a_dispensar').text(datos.monto_a_dispensar)
    $('#folio').text(datos.folio)
    $('#hora_entrada').text(datos.hora_entrada)
    $('#tiempo_estacionado').text(datos.tiempo_estacionado)
    $('#descuento').text(datos.descuento)
        //$("#t1").click(function () {

    if (datos.interfaz == 1) {
        $("#tab-4").prop("checked", true);
    }
    if (datos.interfaz == 2) {
        $("#tab-5").prop("checked", true);
    }
    if (datos.interfaz == 3) {
        $("#tab-6").prop("checked", true);
    }
    if (datos.interfaz == 6) {
        $('[href="#i"]').tab('show')

    }
    if (datos.estado_operacion == 0) {
        $("#status").prop("checked", false);
        $('#mensaje_estado_1').text("Operacion")
        $('#mensaje_estado_2').text("Pausada")
        $('#mensaje_estado_1').attr("fill", "red")
        $('#mensaje_estado_2').attr("fill", "red")

    } else {
        $("#status").prop("checked", true);
        $('#mensaje_estado_1').text("Aplicando")
        $('#mensaje_estado_2').text("Tratamiento")
        $('#mensaje_estado_1').attr("fill", "green")
        $('#mensaje_estado_2').attr("fill", "green")

    }


    // if (datos.presencia == 1) {
    //     $("#presencia").css("background-color", "rgb(51, 214, 51)");
    // }
    // if (datos.retorno == 1) {
    //     $("#retorno").css("background-color", "rgb(51, 214, 51)");
    // }
    // if (datos.boton_ticket == 1) {
    //     $("#boton_ticket").css("background-color", "rgb(51, 214, 51)");
    // }
    // if (datos.secuencia_expedicion == 2) {
    //     $(".insert-ticket").text("Imprmiendo");
    // }
    // if (datos.secuencia_expedicion == 3) {
    //     $(".insert-ticket").text("Lo siento");
    // }
    // if (datos.secuencia_expedicion == 4) {
    //     $(".insert-ticket").text("Bienvenido");
    // }
    // if (datos.secuencia_expedicion == 5) {
    //     $(".insert-ticket").text("Por favor espere...");
    //     $("#img_secuencia_expedicion").attr("src", "{% static 'ui/images/insertar_ticket.gif' %}");
    // }
    //$("#tab-4").prop("checked", true);
    //$("#tab-4").attr("checked", "checked");
    //alert($('input:radio[id=tab-4]:checked').val());
    //$("#tab-4").attr("checked", "checked");

    //	})
    //$('#X_20').text(datos.monto)

    //$('#tabs').tabs('opcion','active',2)
    //$tabs.tabs('select', 1);
    //$("#tabs").tabs("option", "active", 1);

    //var tabs = $("#tabs").tabs();
    //var $tabs = $('#tabs').tabs(); // first tab selected
    //$tabs.tabs('select', 1);

    $('.tabs a[href="#tab-1"]').tab('show')

    //$("#tab-5").prop("checked", false);
    $("#t1").prop("checked", true);

    //var index = $('#tabs a[href="#tab-1"]').parent().index();
    //$("#tabs").tabs("option", "active", index);
}