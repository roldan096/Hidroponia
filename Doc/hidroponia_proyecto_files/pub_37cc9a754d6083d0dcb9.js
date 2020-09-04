function rfsnLoadScript(e,t,a){var n=document.createElement("script");return n.type="text/javascript",n.async=0,n.defer=0,n.readyState?n.onreadystatechange=function(){("loaded"==n.readyState||"complete"==n.readyState)&&(n.onreadystatechange=null,t())}:n.onload=function(){"undefined"!=typeof t&&t()},n.src=e,a?(o=document.getElementsByTagName("script")[0],o.parentNode.insertBefore(n,o)):document.getElementsByTagName("head")[0].appendChild(n),n};


_rfsn_checking=_rfsn_ready=!1;
var _refersion=function(a){if("undefined"===typeof _rfsn_started||!_rfsn_started)rfsnLoadScript("https://trakto.refersion.com/js/xdLocalStorage.min.js?v="+Math.floor(100*Math.random()),function(){xdLocalStorage.init({iframeUrl:"https://trakto.refersion.com/tracker/v3/xdomain/pub_37cc9a754d6083d0dcb9.html",initCallback:function(){rfsnLoadScript("https://trakto.refersion.com/tracker/v3/merchant/pub_37cc9a754d6083d0dcb9.js?v="+Math.floor(100*Math.random()),a)}})}),_rfsn_started=!0;else if(!_rfsn_checking)var b=setInterval(function(){_rfsn_ready&&("function"===typeof a&&
a(),clearInterval(b))},1E3)};

