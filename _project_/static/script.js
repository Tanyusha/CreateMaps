/**
 * Created by Таника on 04.05.2015.
 */
"use strict";

$('.non-checked-btn-for-table').click(function (event) {
    event.preventDefault(); // cancel default behavior
    var table_name = $(this).attr('table-name');
    var p_id = "#p-for-" + table_name;
    var button_id = "#button-close-for-" + table_name;
    $(this).css('display', 'none');
    $(button_id).css('display', 'inline');
    $(p_id).css('display', 'block');
    $(p_id).css('margin', '10px 0 0 0');
});

$('.checked-btn-for-table').click(function (event) {
    event.preventDefault(); // cancel default behavior
    var table_name = $(this).attr('table-name');
    var p_id = "#p-for-" + table_name;
    var button_id = "#button-open-for-" + table_name;
    $(button_id).css('display', 'inline');
    $(this).css('display', 'none');
    $(p_id).css('display', 'none');
});


$('.non-checked-btn-for-field').click(function (event) {
    event.preventDefault(); // cancel default behavior
    var field_name = $(this).attr('field-name');
    var button_id = "#button-close-for-" + field_name;
    $(this).css('display', 'none');
    $(button_id).css('display', 'inline');
});

$('.checked-btn-for-field').click(function (event) {
    event.preventDefault(); // cancel default behavior
    var field_name = $(this).attr('field-name');
    var button_id = "#button-open-for-" + field_name;
    $(button_id).css('display', 'inline');
    $(this).css('display', 'none');
});


function find_spoilers(element) {
    $(element).find(".spoiler").each(function (index, value) {
        var $el = $(value);
        var $title = $el.children('.spoiler__title');
        var $content = $el.children('.spoiler__content');
        $content.toggle("slow");
        $title.click(function () {
            $content.toggle("slow");
        })
    });
}