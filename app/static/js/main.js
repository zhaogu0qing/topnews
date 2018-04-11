/**
 * Created by zhaoguoqing on 18/2/11.
 */

//分栏js

$(document).ready(function () {
  $('[data-toggle="offcanvas"]').click(function () {
    $('.row-offcanvas').toggleClass('active')
  });
});


//md编辑器

// var editor = editormd("editormd", {
//             // width  : "90%",
//             height: 640,
//             saveHTMLToTextarea : true,
//             path : "static/lib/editor.md/lib/"
//         });