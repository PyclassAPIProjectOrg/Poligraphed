$(function() {

    $("#placeholder").bind("plotclick", function (event, pos, item) {
        //alert(item.datapoint + ' ' + item.series.label);
        //alert(item.datapoint[0]);
        submit_form(item.datapoint[0]);
    });

    var cr_markup = function(title, url, speakder) {
        var cr_div = "<div><a target=\"_blank\" href=\""+ url +"\">" + title + "</a><br /><p>"+ speaker_first + " " + speaker_last +"</p></div>";
        return cr_div;
    };

    var submit_form = function(date) {

        $.getJSON($SCRIPT_ROOT + '/_search_cr_api', {
            keyword_1: keyword_1_value,
            keyword_2: keyword_2_value,
            date_low: date,
            date_high: date,
            granularity: granularity_value,

        }, function( data ) {
            $('.cr-records .cr-records-inner').empty();
            $('.cr-records .hidden-container').show();
            for (var a in data.keywords) {
                for (var b in data.keywords[a].results) {
                    title = data.keywords[a].results[b].title;
                    url = data.keywords[a].results[b].origin_url;
                    speaker_first = data.keywords[a].results[b].speaker_first;
                    speaker_last = data.keywords[a].results[b].speaker_last;
                    var cr_record = cr_markup(title, url, speaker_first, speaker_last);
                    $('.cr-records .cr-records-inner').append(cr_record);
                }
            }
            $('.cr-records .hidden-container').hide();
        });

    };

});
