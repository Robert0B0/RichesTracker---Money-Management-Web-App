$(document).ready( function () {
    $('.table_id').DataTable({
    
    dom: 'B<"clear">lfrtip',
    buttons: {
        name: 'primary',
        buttons: [ 'copy', 'csv', 'excel', 'pdf' ]
    
        }}
    );
    } );
       
var rec_titles = JSON.parse("{{rec_names_JSON|escapejs}}");
var rec_starts = JSON.parse("{{rec_start_JSON|escapejs}}");
var rec_value = JSON.parse("{{rec_value_JSON}}");
var rec_len = JSON.parse("{{rec_total_JSON|escapejs}}");
var rec_color = JSON.parse("{{rec_color_JSON|escapejs}}");
var rec_id = JSON.parse("{{rec_id_JSON|escapejs}}");

var recData = [];
for(var i = 0; i < rec_len; i++) {
    recData.push(   {   
                        title: "$" + rec_value[i], 
                        start: rec_starts[i].substring(1, rec_starts[i].length-1),
                        description: "&nbsp record: <u>" + rec_titles[i] + "</u> ,  <br>" + 
                                            " &nbsp valuing: $" + rec_value[i] + " , &nbsp <br> " +
                                            " &nbsp date: " + rec_starts[i].substring(1, rec_starts[i].length-1) + " , &nbsp <br>" +
                                            " &nbsp click to edit. &nbsp",
                        backgroundColor: rec_color[i],
                        backgroundColor: rec_color[i],
                        url: "{% url 'record_form' 123 %}".replace('123', rec_id[i])
                    } 
                ) 
};

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        initialDate: '2020-11-07',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth'
        },  
        events: recData,
        eventClick: function(info) {
        window.location.replace(event.url);
        },
        eventMouseEnter: function(calEvent) {
            var tooltip = '<div class="tooltipevent" style="width:auto; height:auto; vertical-align:middle; position:absolute; background:'+calEvent.el.style.backgroundColor+'; color: white; font-size: 25px !important; font-weight: bold ">' + calEvent.event._def.extendedProps.description + '</div>';
            $("body").append(tooltip);
            $(this.el).mouseover(function(e) {
                $(this.el).css('z-index', 10000);
                $('.tooltipevent').fadeIn('500');
                $('.tooltipevent').fadeTo('10', 1.9);
            }).mousemove(function(e) {
                $('.tooltipevent').css('top', e.pageY + 10);
                $('.tooltipevent').css('left', e.pageX + 20);
            });},
            
            eventMouseLeave: function(calEvent, jsEvent) {
             $(this.el).css('z-index', 8);
             $('.tooltipevent').remove();},
     
    });

    calendar.render();
  });
        
        