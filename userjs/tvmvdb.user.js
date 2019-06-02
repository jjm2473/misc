// ==UserScript==
// @name         tvmvdb
// @namespace    https://github.com/jjm2473
// @version      0.1
// @description  break http://test.tvmvdb.com
// @author       jjm2473
// @downloadURL  https://github.com/jjm2473/misc/raw/master/userjs/tvmvdb.user.js
// @match        http://*.tvmvdb.com/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    window.navSearch = function(){return true};
    window.showPlay = function(){return true};

    var orig = window.$.ajax;
    window.$.ajax = function(p,p2){
        if ("/index.php/Home/play/checkPower" === p.url) {
            if (p.async === false) {
                p.success('allow');
            } else {
                setTimeout(function(){p.success('allow');}, 10);
            }
            return null;
        } else {
            return orig(p, p2);
        }
    };
})();
