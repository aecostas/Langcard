var currentWordIndex=0;
var words = {};
var wordCounter = 0;
var phrase="";

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
	send("SETPHRA"+JSON.stringify(data));
	
	$('#div_processword').hide();	
	$('#div_addword_phrase').show();
	
	$('#input_accept_ok').unbind('click', processWord);
	
	$('#input_accept_ok').click(acceptPhrase);
	cleanup();

    } else {
	$('#foreignword').val(words[currentWordIndex].foreign);
	//$('#foreignword').focus();
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

    if (0 == wordCounter) {
	alert("Select at least one word!");
	return;
    }

    $('#div_selectword_phrase').hide();

    $('#div_selectword_phrase').children().clone().appendTo('#div_currentPhrase');
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

    if (phrase == "") {
	alert("Write a phrase!");
	return;
    }

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


function showAdd() {
    $('#div_addword_phrase').show();
    $('#div_controls').show();
    $('#input_accept_ok').click(acceptPhrase);
    $('#div_main').hide();
    $('#ta_phrase').focus();
}



function cleanup() {
    $('#ta_phrase').text("");
    
    $('#div_selectword_phrase').children().remove();
    $('#table_phrase_list').children().remove();

    currentWordIndex=0;
    words = {};
    wordCounter = 0;
    
}

function home() {
    
    $('#div_processword').hide();	
    $('#div_addword_phrase').hide();
    $('#div_controls').hide();
    $('#div_show_phrase_list').hide();

    $('#input_accept_ok').unbind('click', processWord);
    $('#input_accept_ok').unbind('click', acceptPhrase);
    $('#input_accept_ok').unbind('click', processSelectedWords);
    $('#input_accept_ok').show();
    cleanup();
    
    $('#div_main').show();
}


function showList() {
    send("GETLIST");
    $('#div_main').hide();
    $('#div_show_phrase_list').show();
    $('#div_controls').show();
    $('#input_accept_ok').hide();
}


function setList(lista) {

    phrases = eval('('+lista+')');

    for (elemento in phrases) {
	var str_phrase="";
	var count=0;
	
	var splitted_phrase = phrases[elemento]["phrase"].split(' ');
	
	for (word in splitted_phrase) {
	    str_phrase += "<span>"+splitted_phrase[word]+" </span>";
	}

	$('#table_phrase_list').append('<tr><div id="div_'+phrases[elemento]["id"]+'" class="fila_impar" >'+ str_phrase +'</div> </tr>');

	for (word in phrases[elemento]["words"]) {
	    
	    $('#div_'+phrases[elemento]["id"]+' span:nth-child('+(phrases[elemento]["words"][word]['position']+1)+')').css('color','green');
	    $('#div_'+phrases[elemento]["id"]+' span:nth-child('+(phrases[elemento]["words"][word]['position']+1)+')').attr('title', phrases[elemento]["words"][word]['translation']);

	}

    }// for elemento in phrases
}



$(document).ready(function() {
    $('#mainOption_add').click(showAdd);
    $('#mainOption_list').click(showList);
    
    $('#input_accept_home').click(home);

})
