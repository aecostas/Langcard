var palabras;
var currentWordIndex=0;
var words = {};
var wordCounter = 0;
var phrase;

function processWord() {

    words[currentWordIndex].nativeword = $('#nativeword').val();
    words[currentWordIndex].comments = $.trim($('#ta_comments').val()).replace(/\s+/g,' ').split(' ');
    words[currentWordIndex].value = $('#wordtype').val();

    $('#nativeword').val("");
    $('#ta_comments').val("");

    currentWordIndex++;

    if (currentWordIndex==wordCounter) {
	var data = {};
	
	$('#input_accept_ok').unbind('click', processWord);
	
	data.words = words;
	data.phrase = phrase;
	send(JSON.stringify(data));

	for (i=0; i<wordCounter; i++) {
	    alert(words[i].foreign+"  "+words[i].nativeword);
	}

    } else {
	$('#foreignword').val(words[currentWordIndex].foreign);
    }

}// processWord


function processSelectedWords() {
    // get selected words
    $("[id^=word]").each(function() {
	if ($(this).css('color') == 'rgb(0, 128, 0)') {

	    words[wordCounter] = new Object();
	    words[wordCounter].foreign = $.trim($(this).text());
	    words[wordCounter].position = $("[id^=word]").index($(this));
	    wordCounter++;
	}
	
    });
    
    $('#div_selectword_phrase').hide();
    $('#div_processword').show();	
    
    $('#input_accept_ok').unbind('click', processSelectedWords);
    $('#input_accept_ok').click(processWord);

    $('#foreignword').val(words[0].foreign);

}// processSelectedWords


function selectWord() {

   if ($('#'+this.id).css('color') == 'rgb(0, 128, 0)') {
      $('#'+this.id).css('color','black');
   } else {

      $('#'+this.id).css('color','green');
   }

}// selectWord


function acceptPhrase() {
    // trim, delete repeated whitespace, split into words
    phrase = $.trim($('#ta_phrase').val()).replace(/\s+/g,' ');
    palabras = phrase.split(' ');
    for (i=0; i<palabras.length; i++) {
        $('#div_selectword_phrase').append('<span id=\"word'+i+'\">'+palabras[i]+'</span><span> </span>');
    }

    $('#div_addword_phrase').hide();
    $('#div_selectword_phrase').show();

    $('#input_accept_ok').unbind('click', acceptPhrase);
    $('#input_accept_ok').click(processSelectedWords);

    $("[id^=word]").click(selectWord);
}


$(document).ready(function() {

     $('#input_accept_ok').click(acceptPhrase);
     // http://docs.jquery.com/Events/bind
//     $('#messages').click(got_a_click);
     // http://jollytoad.googlepages.com/json.js provides $.toJSON(...):
     send($.toJSON('document.ready'));
})