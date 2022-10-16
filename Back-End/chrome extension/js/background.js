
const base ="http://127.0.0.1:8000/" //API's url

const urls ={
	'es': base + 'APIRequest/es/',
	'en': base + "APIRequest/en/",
	'ger': base + 'APIRequest/ger/',

	'es-en': base + 'translate/es/en/',
	'es-ger': base + "translate/es/ger/",
	
	'en-es': base + "translate/en/es/",
	'en-ger': base + "translate/en/ger/",

	'ger-es': base + "translate/ger/es/",
	'ger-en': base + "translate/ger/en/",
}; //urls generator



function user_request(obj){
	/*Recives the window object, it filters it and gathers relevant data from it.
	Process the user's request and excecutes it. Finally it replaces the 'entry' container
	*/

	var entry = document.getElementById("entry"); //replaceable (target) container
	var loader = document.getElementsByClassName("loader");

	//Shows a loader as long the request is being processed
	entry.style.display = "none"; //hiddes the entry block as long the request is being processed
	loader[0].style.display = "block"; //shows the loading bar

	//Gathers input's data -> request type, languages involved and the word.
	language_selector = obj.getElementById('lang-selector');
	lang = language_selector.options[language_selector.selectedIndex].value;
	var search = obj.getElementById('user_input');

	//Process the APIRequest.
	const Http = new XMLHttpRequest();
	Http.responseType = "document";

	// const url = urls[lang] + search.value.replace(/\//g, "@"); //Building the url using urls (object)
	// const url = urls[lang] + window.location.href.replace(/\//g, "@"); //Building the url using urls (object)

	chrome.tabs.query({active: true, lastFocusedWindow: true}, tabs => {
    let url = tabs[0].url;
    // use `url` here inside the callback because it's asynchronous!
		Http.open("GET", urls[lang] + url.replace(/\//g, "@"));
		Http.send();
    });


	// Http.open("GET", url);
	// Http.send();

	Http.onreadystatechange = (e) => {
		//Waits until the petition is done and then replace the entry container
		var page = Http.responseXML; //petiton
		var rta=page.getElementById('entry'); //bringing the container from the request
		loader[0].style.display="none"; //hidding the loading spinner
		entry.innerHTML=rta.innerHTML; //replacing the container
		entry.style.display="block"; //showing the entry section again
		search.value=""; //Reseting the input cell

	};

};


//Agregar los EventListener en la ventana popup.html

document.addEventListener('DOMContentLoaded', function () {

	//BOTÓN DE BÚSQUEDA
    var btn = document.getElementById('user_input_button');
    btn.addEventListener("click", () => user_request(this));
    console.log("click event added")


});



