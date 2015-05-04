/**
 * Created by Таника on 04.05.2015.
 */
"use strict";

$('.non-checked-btn-for-table').click(function (event) {
    event.preventDefault(); // cancel default behavior
    var table_name = $(this).attr('table-name');
    var p_id = "#p-for-"+ table_name;
    var button_id = "#button-close-for-"+ table_name;
    $(this).css('display', 'none');
    $(button_id).css('display', 'block');
    $(p_id).css('display', 'block');
    $(p_id).css('margin', '10px 0 0 0');
});

$('.checked-btn-for-table').click(function (event) {
    event.preventDefault(); // cancel default behavior
    var table_name = $(this).attr('table-name');
    var p_id = "#p-for-"+ table_name;
    var button_id = "#button-open-for-"+ table_name;
    $(button_id).css('display', 'block');
    $(this).css('display', 'none');
    $(p_id).css('display', 'none');
});