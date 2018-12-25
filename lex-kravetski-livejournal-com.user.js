// ==UserScript==
// @name          lex-kravetski.livejournal.com
// @description	  L&F
// @author        Yuri Geinish
// @include       https://lex-kravetski.livejournal.com/*
// @run-at        document-start
// @version       0.20181224214657
// ==/UserScript==
(function() {var css = [
	"body, .entry-content, .comment-text {",
	"    font-family: Calibri !important;",
	"}",
	"",
    ".content .entry .entry-text {",
    "    font-size: 10.5pt;",
    "}",
	".entry-content, .comment-text, .sidebar-block dd, .comments-links {",
	"    font-size: 10.5pt !important;",
	"    line-height: 13pt;",
	"}",
	"",
	".comment-upic {",
	"    display: none !important;",
	"}",
	"",
	".comment-head-in {",
	"    margin-left: inherit;",
	"}",
	"",
	".comment-metadata, .comment-poster-info {",
	"    display: inline;",
	"}",
	"",
	"a:visited, a:link {",
	"    border-bottom: none;",
	"    text-decoration: none;",
	"}",
	"",
    "a.comments-pages-button { border-bottom: 1px solid currentColor; }",
	"",
	".entry-content br, .comment-text br {",
	"    line-height: 10pt;",
	"}",
	"",
	".comment-menu, .comment-datetimelink {",
	"    font-size: 9pt;",
	"}",
	"",
	".comment-metadata {",
	"    margin-bottom: 0;",
	"    margin-top: 0;",
	"}",
	"",
	"dl.vcard {",
	"    display: none;",
	"}",
	"",
	"div.lj-like, .entry-linkbar {",
	"    opacity: 0.3;",
	"}",
	"",
	".content-inner, #page, #page .btn-rss span {",
	"    background-color: #FBF8EF;",
	"}",
	"",
	".header .userpic {",
	"    display: none !important;",
	"}",
    ".comment-text blockquote { margin-bottom: 0; background-color: #F5ECCE; border-left: 2px solid grey; }"
].join("\n");
if (typeof GM_addStyle != "undefined") {
	GM_addStyle(css);
} else if (typeof PRO_addStyle != "undefined") {
	PRO_addStyle(css);
} else if (typeof addStyle != "undefined") {
	addStyle(css);
} else {
	var node = document.createElement("style");
	node.type = "text/css";
	node.appendChild(document.createTextNode(css));
	var heads = document.getElementsByTagName("head");
	if (heads.length > 0) {
		heads[0].appendChild(node);
	} else {
		// no head yet, stick it whereever
		document.documentElement.appendChild(node);
	}
}

function prettifyDom() {
    function textToHtml(text) {
        var p = document.createElement("p");
        p.innerText = text;
        return p.innerHTML;
    }

    var comments = document.getElementsByClassName("comment-text");
    for (var commentIdx = 0; commentIdx < comments.length; commentIdx++) {
        var comment = comments[commentIdx];
      
        /* Avoid destroying single-image comments. */
        if (comment.innerText.length == 0) {
            continue;
        }

        var modified = false;
        var lines = comment.innerText.split("\n");
        for (var lineIdx = 0; lineIdx < lines.length; lineIdx++) {
            var line = lines[lineIdx];
            if (line.startsWith(">")) {
                lines[lineIdx] = "<blockquote>" + textToHtml(line.substring(1)) + "</blockquote>";
                modified = true;
            } else {
              lines[lineIdx] = textToHtml(line) + "<br/>";
            }
        }
        if (modified) {
            comment.innerHTML = lines.join("");
        }
    }    
}

document.addEventListener("DOMContentLoaded", function() {
  prettifyDom();
  document.addEventListener("DOMNodeInserted", prettifyDom);
});

})();
