$(function() {

    var date_value_input = function(input, days_back) {
        var now = new Date();
        now.setDate(now.getDate() - days_back);
        var day = ("0" + now.getDate()).slice(-2);
        var month = ("0" + (now.getMonth() + 1)).slice(-2);
        var today = now.getFullYear()+"-"+(month)+"-"+(day) ;
        input.val(today);
    };

    var submit_form = function(testing) {
      var dates = [];
      var more_dates = [];
      var tickarray = null;

      keyword_1_value = testing.closest('form').find( $('input[name="keyword_1"]')).val();
      keyword_2_value = testing.closest('form').find( $('input[name="keyword_2"]')).val();
      date_low_value = testing.closest('form').find( $('input[name="date_low"]')).val();
      date_high_value = testing.closest('form').find( $('input[name="date_high"]')).val();
      granularity_value = testing.closest('form').find( $('select[name="granularity"]')).val();

      //Set timeformat based on granularity
      if (granularity_value == 'day'){
        timeformat = "%b %e";
        granularity = 'day';
      } else if(granularity_value == 'month'){
        timeformat = "%b %Y";
        granularity = 'month';
      } else if(granularity_value == 'year'){
        timeformat = "%Y";
        granularity = 'year';
      }

      $('.graph-container .hidden-container').show();

      $.getJSON($SCRIPT_ROOT + '/_search_api', {

        keyword_1: keyword_1_value,
        keyword_2: keyword_2_value,
        date_low: date_low_value,
        date_high: date_high_value,
        granularity: granularity_value,

      }, function(data) {

        $("#result").empty();

        //Flot adds multiple ticks for months when less than or equal to 8 month/year points
        for (var a in data.keywords) {

          if (data.keywords[a].results.length <= 8 && a === "0"){
            tickarray = [];
          }

          for (var b in data.keywords[a].results) {

             //Custom array supplied to xaxis ticks when less than or equal to 8 month/year points
            if (data.keywords[a].results.length <= 8 && a === "0"){
              tickarray.push([data.keywords[a].results[b][granularity]]);
            }

            if (a === "0") {
              dates.push([data.keywords[a].results[b][granularity], data.keywords[a].results[b].count]);

            } else if (keyword_2_value !== "") {
              more_dates.push([data.keywords[a].results[b][granularity], data.keywords[a].results[b].count]);
            }
          }
        }
            if(keyword_2_value !== ""){
              $("#keyword").text(keyword_1_value +" vs. " + keyword_2_value);
            } else{
              $("#keyword").text(keyword_1_value);
            }

            $.plot($("#placeholder"),
              [ { label: keyword_1_value, data: dates },
                { label: keyword_2_value, data: more_dates }
              ],
              { xaxis: {
                  mode: "time",
                  timeformat: timeformat,
                  ticks: tickarray
                },
                lines: {
                  show: true
                },
                points: {
                  show: true
                },
              grid: {
                hoverable: true,
                clickable: true,
                borderWidth: 1,
                minBorderMargin: 20,
                labelMargin: 10,
                axisMargin: 8,
                        },
                margin: {
                  top: 8,
                  bottom: 20,
                  left: 20
                },
              legend: {
                  show: true,
                  // labelFormatter: null or (fn: string, series object -> string)
                  // labelBoxBorderColor: #000,
                  // noColumns: number
                  position: "ne",
                  // margin: number of pixels or [x margin, y margin]
                  backgroundColor: "white",
                  backgroundOpacity: .5
                  // container: null or jQuery object/DOM element/jQuery expression
                  // sorted: null/false, true, "ascending", "descending", "reverse", or a comparator
              }
            }
          );

        $('.graph-container .hidden-container').hide();
        $('#result').text(data.user);
        $('input[name=a]').focus().select();

        $('.save-graph-button').show();
        //Add ajax input fields to hidden SavedGraph inputs
        $("#saved_graph_form-graph_name").prop('required',true);
        $("#saved_graph_form-submit").addClass('btn-success');
        $('#saved_graph_form-keyword_1, #keyword_1').val(keyword_1_value);
        $('#saved_graph_form-keyword_2, #keyword_2').val(keyword_2_value);
        $('#saved_graph_form-date_low, #date_low').val(date_low_value);
        $('#saved_graph_form-date_high, #date_high').val(date_high_value);
        $('#saved_graph_form-granularity, #granularity').val(granularity_value);

      });
      return false;
    };

    $('.make_graph').click(function(){
      testing = $(this);
      submit_form(testing);
    });

    $(window).resize(function(){
      testing = $('#calculate');
      submit_form(testing);
    });

    $('input[name=a]').focus();

    $.plot($("#placeholder"), [[0,0]],
            {
              grid: {
                hoverable: true,
                clickable: true,
                borderWidth: 1,
                minBorderMargin: 20,
                labelMargin: 10,
                axisMargin: 8,
                        },
                margin: {
                  top: 8,
                  bottom: 20,
                  left: 20
                },
              }
      );

   date_value_input($('#date_low'), 30);
   date_value_input($('#date_high'), 0);

});
