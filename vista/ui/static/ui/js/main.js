(function($) {

    var form = $("#signup-form");
    form.validate({
        errorPlacement: function errorPlacement(error, element) {
            element.before(error);
        },
        rules: {
            first_name: {
                required: true,
            },
            last_name: {
                required: true,
            },
            email: {
                required: true,
                email: true
            }
        },
        messages: {
            first_name: {
                required: "Please enter your first name"
            },
            last_name: {
                required: "Please enter your last name"
            },
            email: {
                required: "Please enter your first name",
                email: "Please enter a valid email address!"
            }
        },
        onfocusout: function(element) {
            $(element).valid();
        },
        highlight: function(element, errorClass, validClass) {
            $(element).parent().parent().find('.form-group').addClass('form-error');
            $(element).removeClass('valid');
            $(element).addClass('error');
        },
        unhighlight: function(element, errorClass, validClass) {
            $(element).parent().parent().find('.form-group').removeClass('form-error');
            $(element).removeClass('error');
            $(element).addClass('valid');
        }
    });
    form.steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        labels: {
            previous: 'Previous',
            next: 'Next',
            finish: 'Finish',
            current: ''
        },
        titleTemplate: '<h3 class="title">#title#</h3>',
        onInit: function(event, currentIndex) {
            // Suppress (skip) "Warning" step if the user is old enough.
            if (currentIndex === 0) {
                form.find('.actions').addClass('test');
            }
        },
        onStepChanging: function(event, currentIndex, newIndex) {
            form.validate().settings.ignore = ":disabled,:hidden";
            return form.valid();
        },
        onFinishing: function(event, currentIndex) {
            form.validate().settings.ignore = ":disabled";
            return form.valid();
        },
        onFinished: function(event, currentIndex) {
            alert('Sumited');
        },
        onStepChanged: function(event, currentIndex, priorIndex) {


        }
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });

    // $('#country').parent().append('<ul id="newcountry" class="select-list" name="country"></ul>');
    // $('#country option').each(function(){
    //     $('#newcountry').append('<li value="' + $(this).val() + '">'+$(this).text()+'</li>');
    // });
    // $('#country').remove();
    // $('#newcountry').attr('id', 'country');
    // $('#country li').first().addClass('init');
    // $("#country").on("click", ".init", function() {
    //     $(this).closest("#country").children('li:not(.init)').toggle();
    // });

    // var allOptions = $("#country").children('li:not(.init)');
    // $("#country").on("click", "li:not(.init)", function() {
    //     allOptions.removeClass('selected');
    //     $(this).addClass('selected');
    //     $("#country").children('.init').html($(this).html());
    //     allOptions.toggle();
    // });

    // var inputs = document.querySelectorAll( '.inputfile' );
    // Array.prototype.forEach.call( inputs, function( input )
    // {
    // 	var label	 = input.nextElementSibling,
    // 		labelVal = label.innerHTML;

    // 	input.addEventListener( 'change', function( e )
    // 	{
    // 		var fileName = '';
    // 		if( this.files && this.files.length > 1 )
    // 			fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
    // 		else
    // 			fileName = e.target.value.split( '\\' ).pop();

    // 		if( fileName )
    // 			label.querySelector( 'span' ).innerHTML = fileName;
    // 		else
    // 			label.innerHTML = labelVal;
    // 	});

    // 	// Firefox bug fix
    // 	input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
    // 	input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
    // });


})(jQuery);

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
            $('.your_picture_image')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}


FusionCharts.ready(function() {
  var myChart = new FusionCharts({
    id: "stockRealTimeChart",
    type: 'realtimeline',
    renderAt: 'chart-container',
    width: '500',
    height: '300',
    dataFormat: 'json',
    dataSource: {
      "chart": {
        "caption": "Real-time stock price monitor",
        "subCaption": "Harry's SuperMart",
        "xAxisName": "Time",
        "yAxisName": "Stock Price",
        "numberPrefix": "$",
        "refreshinterval": "5",
        "yaxisminvalue": "35",
        "yaxismaxvalue": "36",
        "numdisplaysets": "10",
        "labeldisplay": "rotate",
        "showValues": "0",
        "showRealTimeValue": "0",
        "theme": "fusion"
      },
      "categories": [{
        "category": [{
          "label": "Day Start"
        }]
      }],
      "dataset": [{
        "data": [{
          "value": "35.27"
        }]
      }]
    },
    "events": {
      "initialized": function(e) {
        var flag = 0;

        function addLeadingZero(num) {
          return (num <= 9) ? ("0" + num) : num;

        }

        function updateData() {
          // Get reference to the chart using its ID
          var chartRef = e.sender,
            // We need to create a querystring format incremental update, containing
            // label in hh:mm:ss format
            // and a value (random).
            currDate = new Date(),
            label = addLeadingZero(currDate.getHours()) + ":" +
            addLeadingZero(currDate.getMinutes()) + ":" +
            addLeadingZero(currDate.getSeconds()),
            // Get random number between 35.25 & 35.75 - rounded to 2 decimal places
            randomValue = Math.floor(Math.random() * 50) / 100 + 35.25,

            // Build Data String in format &label=...&value=...
            strData = "&label=" + label + "&value=" + randomValue;
          flag = flag + 1;
          if (flag % 7 === 0) {
            strData = "&label=" + label + "&value=" + randomValue + "&vline=1&vLineLabel=Price Checked&vLineColor=#666666&vLineThickness=2&vLineDashed=1";
          }
          // Feed it to chart.
          chartRef.feedData(strData);
        }

        e.sender.chartInterval = setInterval(function() {
          updateData();
        }, 5000);
      },
      "disposed": function(evt, args) {
        clearInterval(evt.sender.chartInterval);
      }
    }
  }).render();
});
