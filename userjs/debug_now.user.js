// ==UserScript==
// @name         Debug now
// @namespace    http://jjm2473.github.io/
// @version      0.1
// @description  跟踪获取当前时间的脚本，将需要跟踪的网站添加到"用户包括"或"用户匹配"列表
// @author       jjm2473
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    var Date = window.Date;
    var now = function(){
        console.trace('get Now');
        return Date.now();
    };
    var NewDate = function(s) {
        if (typeof s === "undefined") {
            return new Date(now());
        } else {
            return new Date(s);
        }
    };
    NewDate.now = now;
    window.Date = NewDate;
})();
