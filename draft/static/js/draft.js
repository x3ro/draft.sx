var Gisted = (function($, undefined) {
    var gist = function(gist_id) {
        if($('section.content').data('loaded')) {
            triggerLoadEmbeddedGists();
            return;
        }

        var gistxhr = $.getJSON('/' + gist_id + '/content')
            .done(function(data, textStatus, xhr) {

                if(typeof(data['owner']) !== 'undefined' && data['owner'] !== null) {
                    var author = data['owner']['login'];
                    var url = data['owner']['html_url'];
                    var $authorLink = $("#author-link");
                    $authorLink.text(author).attr('href', url);
                }

                var description = data['description'];
                if (description) {
                    $("#description").text(description);
                    document.title = document.title.replace("#" + gist_id, description);
                } else {
                    $("#description").text('');
                }
                var files = data['files'];
                var keys = Object.keys(files);
                var empty = true;
                for (var i=0; i<keys.length; i++) {
                    var file = files[keys[i]];
                    if (file['rendered']) {
                        empty = false;
                        var filediv = $('<article>')
                            .attr('class', 'file')
                            .attr('data-filename', file['filename']);
                        filediv.html("<h1>" + file['filename'] + "</h1>" + file['rendered']);
                        $('#gistbody').append(filediv);
                    }
                }
                if (empty) {
                    apologize("No Content Found");
                }

                triggerLoadEmbeddedGists();
            })
            .fail(function(xhr, status, error) {
                if (xhr.status == 404) {
                    apologize("No Content Found");
                } else {
                    apologize("Unable to Fetch Gist");
                }
            })
            .always(function() {
                $("#description").removeClass("loading");
                $(".content>footer").fadeIn();
            });
    };
    var apologize = function(errorText) {
        $("#description").text(errorText);
        var apology = $('<p>').attr('class', 'apology').text("Quite flummoxed. Terribly sorry.");
        $('#gistbody').append(apology);
    };
    return {
        gist: gist
    };
})(jQuery);
