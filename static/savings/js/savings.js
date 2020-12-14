$(document).ready( function () {
    $('.table_id').DataTable({
    
    dom: 'B<"clear">lfrtip',
    buttons: {
        name: 'primary',
        buttons: [ 'copy', 'csv', 'excel', 'pdf' ]
    
        }}
    );
    } );