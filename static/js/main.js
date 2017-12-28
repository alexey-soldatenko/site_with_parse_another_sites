// возвращает cookie с именем name, если есть, если нет, то undefined
	function getCookie(name) {
	  var matches = document.cookie.match(new RegExp(
	    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
	  ));
	  return matches ? decodeURIComponent(matches[1]) : undefined;
	}

var csrftoken = getCookie('csrftoken');
			var httpRequest = new XMLHttpRequest();
			httpRequest.open('POST', '/last_date', true);

			httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
			httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
			httpRequest.setRequestHeader('X-CSRFToken', csrftoken);
			httpRequest.onreadystatechange = function(){
				if (httpRequest.readyState == 4 && httpRequest.status == 200){
					date = httpRequest.responseText;
				}
				
			}
			httpRequest.send();
try{
	setInterval(function(){
			var data = "last_date="+encodeURIComponent(date);
			var csrf_token = getCookie('csrftoken');

			var httpRequest = new XMLHttpRequest();
			httpRequest.open('POST', '/', true);

			httpRequest.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
			httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
			httpRequest.setRequestHeader('X-CSRFToken', csrftoken);

			httpRequest.onreadystatechange = function(){
				if (httpRequest.readyState == 4 && httpRequest.status == 200){
					answer = JSON.parse(httpRequest.responseText);
					
					var block1 = document.getElementById('area_left');
					block1.innerHTML += answer['block1'];
					block1.scrollTop = block1.scrollHeight;

					var block2 = document.getElementById('area_right');
					block2.innerHTML += answer['block2'];
					block2.scrollTop = block2.scrollHeight;

					date = answer['new_date'];
					
				}
				
			}
			httpRequest.send(data);
		}
		, 5000);
}

catch(err){
	alert(err);
}