jQuery(function ($) {

    'use strict';

    (function () {
        var today = new Date();
    
        var launch = new Date("July 01, 2018");
        var msPerDay = 24 * 60 * 60 * 1000;
        var timeLeft = (launch.getTime() - today.getTime());
    
        var e_daysLeft = timeLeft / msPerDay;
        var daysLeft = Math.floor(e_daysLeft);

        $('.calendar .left').text(daysLeft);
    })();
}); // JQuery end

