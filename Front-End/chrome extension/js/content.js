
const APIURL='http://127.0.0.1:8000/newEntry/es/'

function StringCleaner(obj){
	/*
	Limpia el string de todo caracter especial
	Devuelve un string con la palabra pura
	Ejemplo objeto->"casa"
	*/
	let regex = /^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$/g;

	return obj.innerHTML.replace(/:|(|)|{|}|/g, "").replace(".","").replace(",","");
};

function APICall(obj){
	console.log(StringCleaner(obj));
	const Http = new XMLHttpRequest();
	Http.responseType="document";
	const url=APIURL+obj.innerHTML;
	Http.open("GET", url);
	Http.send();

	Http.onreadystatechange = (e) => {
		var page = Http.responseXML;
		var rta=page.getElementById("definition");
		console.log(rta)
	};
};

function input_filler (obj){
	var word = obj.innerHTML
	console.log(word);
}

var parrafos = document.getElementsByTagName('p');

//TOKENIZACIÓN DEL PÁRRAFO
for (let parrafo=0 ; parrafo < parrafos.length; parrafo++){

	//Convertir objeto párrafo a array de texto
	var parrafoText=parrafos[parrafo].innerText.split(" ");

	var temporal = [];
	//Por cada palabra en el array, crear objeto y almacenarlo en una lista temporal
	for (let palabra=0 ; palabra< parrafoText.length; palabra++){

		//Tokenización del párrafo
		var nuevoSpan=document.createElement('span');
		nuevoSpan.innerHTML=parrafoText[palabra];
		//EventListener, onclick send object
		nuevoSpan.addEventListener("click", () => input_filler(this.event.path[0]),false);
		temporal.push(nuevoSpan);

	};
	//Crear nuevo párrafo
	var nuevoElemento = document.createElement('p');

	for (let i=0 ; i < temporal.length ; i++){
		//Agregar cada objeto span finalizado al p padre
		nuevoElemento.appendChild(temporal[i]);

		//Separador -> espacio
		var space=document.createElement('span');
		space.innerHTML=' ';
		nuevoElemento.appendChild(space);
	};

	//Reemplazar párrafo anterior con el nuevo
	parrafos[parrafo].replaceWith(nuevoElemento);

};
