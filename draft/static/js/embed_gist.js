;(function($) {

    function EmbedGist($element) {
        var that = this;

        this.id = $element.text();

        this.$container = $('<div>')
            .addClass('loading-embedded-gist')
            .insertAfter($element);
        $element.remove();

        $.get('/embed_gist/' + this.id)
            .success(function(script) {
                that.prepareEvalGist();
                eval(script);
                that.unprepareEvalGist();
            })

            .always(function() {
                that.$container.removeClass('loading-embedded-gist');
            });
    }

    EmbedGist.prototype = {
        prepareEvalGist: function() {
            var that = this;
            this.documentWriteBackup = document.write;
            document.write = function(markup) {
                var html = that.$container.html();
                that.$container.html(html + markup);
            }
        },

        unprepareEvalGist: function() {
            document.write = this.documentWriteBackup;
        }
    };



    window.triggerLoadEmbeddedGists = function() {
        $('gist').each(function() { new EmbedGist($(this)) });
    }

})(jQuery);
