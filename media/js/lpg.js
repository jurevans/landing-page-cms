// /media/js/lpg.js

$(document).ready(function(){
    
    $('#id_body').addClass('tinymce');
    $('#id_call_to_action_form').addClass('no_tinymce');
    $('#id_google_analytics_form').addClass('no_tinymce');
    $('#id_background_color').addClass('color');
    $('#add_id_layout').hide();
    
    var logo = '/media/' + $('div.logo div a').url();
    if($('div.logo div a')[0])
    {
        $('div.logo div a')[0].href=logo;
    }
    
    var background = '/media/' + $('div.form-row.background_image a').url();
    if($('div.form-row.background_image a')[0])
    {
        $('div.form-row.background_image a')[0].href=background;
    }
    
    var photo = '/media/' + $('div.form-row.photo a').url();
    if($('div.form-row.photo a')[0])
    {
        $('div.form-row.photo a')[0].href=photo;
    }
    
    var max_fields = function(field, max_char)
    {
        $(field).each(function(){
            $(this).parent().append($('<p><strong>' + max_char + '</strong> characters max.<br /><strong><span class="number">0</span></strong> characters.</p>'));
            
            // Initialize new elements
            var counter = $(this).parent().find('.number');
            var x = parseInt($(this).val().length);
            
            counter.text(x);
            if(x >= max_char)
            {
                $(counter).css('color', '#cc0000');
            }
            
            $(this).keyup(function(){
                var counter = $(this).parent().find('.number');
                var x = parseInt($(this).val().length-1);
                
                $(counter).text(x + 1);
                
                if(x >= max_char)
                {
                    $(counter).css('color', '#cc0000');
                }
                else
                {
                    $(counter).css('color', '');
                }
                return true;
            });
                
        });
    };
    
    max_fields('#id_meta_description', 250);
    max_fields('#id_meta_keywords', 250);
    max_fields('#id_footer', 250);
    
    if($('.toggle_media select'))
    {
        if(!$('.toggle_media select').val())
        {
            $('div.photo').hide();
            $('div.embed_media').hide();
        }
        else if($('.toggle_media select').val() == 'P')
        {
            $('div.photo').show();
            $('div.embed_media').hide();
        }
        else if($('.toggle_media select').val() == 'E')
        {
            $('div.photo').hide();
            $('div.embed_media').show();
        }
        // Let's toggle the Media inputs!
        
        $('.toggle_media select').change(function(){
            // null = null
            // 0 = Photo
            // 1 = Embed
            var curr_val = $(this).val();
            if(curr_val==null || curr_val=='')
            {
                $('div.photo').hide();
                $('div.embed_media').hide();
            }
            else if(curr_val == 'P')
            {
                $('div.photo').show();
                $('div.embed_media').hide();
            }
            else if(curr_val == 'E')
            {
                $('div.photo').hide();
                $('div.embed_media').show();
            }
        });
    }
    
    // Hide fields in Admin:
    // Actually, nah, use FIELD_SETS!
    //if($('div.num_pages'))
    //{
    //    $('div.num_pages').hide();
    //}
    
});


// Tool-tip inititialization // Uncomment below to enable tool-tips.

$(function(){
    $("label").tooltip({
        bodyHandler: function() {
            //return $(this).parent().find('.help').html();
            return($(this).parent().find('.help').html());
        },
        showURL: false
    });
  
});

// Administrative text entry
// TinyMCE initialization

tinyMCE.init({
    mode : "textareas",
    theme : "advanced",
    editor_selector : "tinymce",
    editor_deselector : "no_tinymce",
    //content_css : "/appmedia/blog/style.css",
    theme_advanced_toolbar_location : "top",
    theme_advanced_toolbar_align : "left",
    //theme_advanced_buttons1 : "fullscreen,separator,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,image,cleanup,help,separator,code",
    theme_advanced_buttons1 : "fullscreen,separator,bold,italic,underline,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,cleanup,help",
    theme_advanced_buttons2 : "",
    theme_advanced_buttons3 : "",
    auto_cleanup_word : true,
    //plugins : "table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,preview,zoom,flash,searchreplace,print,contextmenu,fullscreen",
    plugins : "table,save,advhr,insertdatetime,preview,zoom,flash,searchreplace,print,contextmenu,fullscreen",
    plugin_insertdate_dateFormat : "%m/%d/%Y",
    plugin_insertdate_timeFormat : "%H:%M:%S",
    extended_valid_elements : "a[name|href|target=_blank|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]",
    fullscreen_settings : {
        theme_advanced_path_location : "top"//,
        //theme_advanced_buttons1 : "fullscreen,separator,preview,separator,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help",
        //theme_advanced_buttons2 : "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor",
        //theme_advanced_buttons3 : "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"
    }
});
