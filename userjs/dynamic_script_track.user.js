// ==UserScript==
// @name         Eval tracker
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       jjm2473
// @match        https://wiki.biligame.com/ys/%E5%8E%9F%E7%A5%9E%E5%9C%B0%E5%9B%BE%E5%B7%A5%E5%85%B7_%E5%85%A8%E5%9C%B0%E6%A0%87%E4%BD%8D%E7%BD%AE%E7%82%B9
// @icon         https://www.google.com/s2/favicons?domain=biligame.com
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function() {

    var script_track = function(tag, s) {
        return "console.trace('" + tag + "');\n" + (s || "");
    };

    var oeval = window.eval;
    var eval = (function() {
        try{
            return oeval(script_track("Eval Track", arguments[0]));
        }catch(e){
            console.error(e);
            console.log(arguments[0]);
            debugger;
        }
    });//.bind(null);
    eval.toString = oeval.toString;
    eval.prototype = undefined;
    //window.eval = eval; //eval must run in caller's scope, we can't do that

    var Function = window.Function;
    window.Function = function(s) {
        return Function.call(this, script_track("Function Track", s));
    };
    window.Function.prototype = Function.prototype;

    var textsetter = window.HTMLScriptElement.prototype.__lookupSetter__('text') || function(text) { this.text = text ; return text;}
    window.HTMLScriptElement.prototype.__defineSetter__('text', function(text) {
        return textsetter.call(this, script_track("Script Track", text));
    });


})();
