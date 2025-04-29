// ==UserScript==
// @name         gd2m3u8
// @namespace    http://github.com/jjm2473/
// @version      2025-04-29
// @description  download m3u8 from 120.76.248.139
// @author       jjm2473
// @match        http://120.76.248.139/udp/udp_channel_list.php?*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    var page2m3u8=function(){
        var groups=document.body.querySelectorAll('.channel-list');
        var flaten=groups.entries().flatMap((a)=>{
            var group=a[1].id;
            var details=a[1].querySelectorAll('.channel-item>.details');
            return details.entries().map(d=>{
                var name = d[1].children[0].innerText;
                var proxy=d[1].children[1].innerText;
                var stream=d[1].children[2].innerText;
                var url = 'http://'+proxy+'/'+stream.replace('udp://', 'rtp://').replace('://', '/');
                return {
                    group,
                    name,
                    url
                };
            });
        }).toArray();
        return flaten.reduce((m,d)=>m+'#EXTINF:-1, group-title="'+d.group+'", '+d.name+'\n'+d.url+'\n\n', '#EXTM3U\n\n');
    };
    var downloadHelper=document.createElement('a');
    downloadHelper.target='_blank';
    downloadHelper.download='file';
    downloadHelper.style='display: none';
    document.body.appendChild(downloadHelper);

    var button=document.createElement('button');
    button.innerText='M3U8';
    button.style='position: fixed; right: 0;top: 0; cursor: pointer;';
    button.onclick=()=>{
        var match=document.body.querySelector('.search-container').innerText.match(/当前是([^\n]+)的组播地址/);
        var filename='test';
        if (match && match.length==2) {
            filename=match[1];
        }
        var m3u8 = page2m3u8();
        var blob = new Blob([m3u8], {type:'text/plain'});
        var url = URL.createObjectURL(blob);
        downloadHelper.href = url;
        downloadHelper.download = filename+'.m3u8';
        downloadHelper.click();
    };
    document.body.appendChild(button);

})();
