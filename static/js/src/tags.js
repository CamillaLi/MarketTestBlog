var TAG_TEMPLATE = "<dt><a href='/tag/{tag}/'>{tag}</a></dt><dd>{count}<dd>";
var AUTHOR_TEMPLATE = "<dt><a href='/author/{author}/'>{author}</a></dt><dd>{count}<dd>";
function renderTags(data){
    var tagsHtml = "";
    for (var key in data) {
        tagsHtml += TAG_TEMPLATE.replace(/\{tag}/g, key)
            .replace(/\{count}/g, data[key].length);
    }
    $("#tags").html(tagsHtml);
}
function renderAuthors(data){
    var authorsHtml = "";
    for (var key in data) {
        authorsHtml += AUTHOR_TEMPLATE.replace(/\{author}/g, key)
            .replace(/\{count}/g, data[key].length);
    }
    $("#authors").html(authorsHtml);
}

$(document).ready(function() {
    var url = "/api/index/inv_tag/";
    var url2 = "/api/index/inv_author/";
    $.ajax({
        type: "get",
        dateType: "json",
        url: url,
        success: function(data) {
            renderTags(data);
        }
    });
    $.ajax({
        type: "get",
        dateType: "json",
        url: url2,
        success: function(data) {
            renderAuthors(data);
        }
    });
});


