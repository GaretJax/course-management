/*
 * Copyright (c) 2013, Divio AG
 * Licensed under BSD
 * http://github.com/aldryn/aldryn-boilerplate-bootstrap3
 */

// #############################################################################
// NAMESPACES
/**
 * @module Cl
 */
// istanbul ignore next
var Cl = window.Cl || {};
/* global outdatedBrowser */

// #############################################################################
// BASE
// istanbul ignore next
(function ($) {
    'use strict';

    // shorthand for invoking jQuery(document).ready
    $(function () {
        // removes noscript form body and adds print-js
        if (window.Cl && window.Cl.Utils) {
            Cl.Utils._document();
        }

        // DOCS: https://github.com/burocratik/outdated-browser
        if (window.outdatedBrowser) {
            outdatedBrowser({
                'languagePath': '',
                'lowerThan': 'boxShadow'
            });
        }

        // submit forms when clicking on buttons outside them
        $('.btn-submit').click(function () {
            var formId = $(this).attr('rel');
            $('form#' + formId).submit();
        });

        // autosubmit form on change
        $('.autosubmit input, .autosubmit select').change(function () {
            $(this).closest('form').submit()
        });

        // toggle checkbox inside cell on click
        $('td.toggle-checkbox').click(function () {
            $(this).find('input[type=checkbox]').trigger('click');
        });
        $('td.toggle-checkbox input[type=checkbox]').click(function (e) {
            e.stopPropagation();
        });

        // date/time pickers
        $('.datetimepicker').datetimepicker({
            icons: {
                time: 'fa fa-clock-o',
                date: 'fa fa-calendar',
                up: 'fa fa-chevron-up',
                down: 'fa fa-chevron-down',
                previous: 'fa fa-chevron-left',
                next: 'fa fa-chevron-right',
                today: 'fa fa-bullseye',
                clear: 'fa fa-trash-o',
                close: 'fa fa-remove'
            },
            locale: moment.locale('it'),
            calendarWeeks: true,
            showClose: true,
            //showTodayButton: true,
            allowInputToggle: true,
        });
    });

})(jQuery);
