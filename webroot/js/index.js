$(document).ready(function(){
  
    
  var dropbox = $('#uploader');
	
	dropbox.filedrop({
		// The name of the $_FILES entry:
		paramname:'pic',

		maxfiles: 5,
    	maxfilesize: 2,
		url: 'post_file.php',

		uploadFinished:function(i,file,response){
			$.data(file).addClass('done');
			// response is the JSON object that post_file.php returns
		},

    error: function(err, file) {
			switch(err) {
				case 'BrowserNotSupported':
					showMessage('Your browser does not support HTML5 file uploads!');
					break;
				case 'TooManyFiles':
					alert('Too many files! Please select 5 at most! (configurable)');
					break;
				case 'FileTooLarge':
					alert(file.name+' is too large! Please upload files up to 2mb (configurable).');
					break;
				default:
					break;
			}
		},

		// Called before each upload is started
		beforeEach: function(file){
			if(!file.type.match(/^image\//)){
				//alert('Only images are allowed!');
        $('#uploader').removeClass('active');
				// Returning false will cause the
				// file to be rejected
				return false;
			}
		},

		uploadStarted:function(i, file, len){
			createImage(file);
		},

		progressUpdated: function(i, file, progress) {
			$.data(file).find('.progress').width(progress);
		},
		
		dragOver: function(){
		  $('#uploader').addClass('active');
		},
		
		dragLeave: function(){
		  $('#uploader').removeClass('active');
		}

	});
})