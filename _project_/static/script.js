/**
 * Created by Таника on 04.05.2015.
 */
"use strict";

$('.non-checked-btn-for-table').click(function (event) {
    event.preventDefault(); // cancel default behavior
    var table_name = $(this).attr('table-name');
    var p_id = "#p-for-"+ table_name;
    var span_id = "#span-for-"+ table_name;
    $(this).removeClass('non-checked-btn-for-table');
    $(this).addClass('checked-btn-for-table');
    $(p_id).css('display', 'block');
    $(p_id).css('margin', '10px 0 0 0');
    $(span_id).removeClass('glyphicon-plus');
    $(span_id).addClass('glyphicon-minus');
});

$('.checked-btn-for-table').click(function (event) {
    alert("lalal");
    event.preventDefault(); // cancel default behavior
    var table_name = $(this).attr('table-name');
    var p_id = "#p-for-"+ table_name;
    var span_id = "#span-for-"+ table_name;
    $(this).removeClass('checked-btn-for-table');
    $(this).addClass('non-checked-btn-for-table');
    alert("lalal");
    $(p_id).css('display', 'none');
    $(span_id).removeClass('glyphicon-minus');
    $(span_id).addClass('glyphicon-plus');
});
