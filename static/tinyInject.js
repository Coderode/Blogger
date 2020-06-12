
//to inject tinyMCE texteditor in the admin panel of post textarea 
//so that the user can post designed posts from the panel
//this script this actually creating a script tag in the header of the page in the admin panel to inject the editor there
//<script src="https://cdn.tiny.cloud/1/no-api-key/tinymce/5/tinymce.min.js" referrerpolicy="origin"></script>

var script = document.createElement('script');
script.type ='text/javascript';
script.src= "https://cdn.tiny.cloud/1/3efd2jpvatfkuyju1odxc59ndtqmrd6iagqpnt7d005qiwra/tinymce/5/tinymce.min.js";
document.head.appendChild(script);
//extras to add plug in in the editor see the documentation of the tiny MCE for this
script.onload = function(){
    tinymce.init({
        selector: '#id_content',  //id_content is id of the textarea in the admin panel of post
        height:600,
        plugins: [
            'advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker',
            'searchreplace wordcount visualblocks visualchars code fullscreen insertdatetime media nonbreaking',
            'table emoticons template paste help'
        ],
        toolbar: 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | ' +
        'bullist numlist outdent indent | link image | print preview media fullpage | ' +
        'forecolor backcolor emoticons | help',
        menu: {
            favs: {title: 'My Favorites', items: 'code visualaid | searchreplace | spellchecker | emoticons'}
        },
        menubar: 'favs file edit view insert format tools table help',
        content_css: 'css/content.css'
    });
}




  //now inject in the blog : beacause the blog is modal of the blog app
  // so inject it through  the admin of the blog app
