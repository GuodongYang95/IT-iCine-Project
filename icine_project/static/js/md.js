$(function(){

    $(".navbar-left li").click(toggleSidebar);
});
 

function toggleSidebar(){
    $("body").toggleClass("big-page");
    return false;
}