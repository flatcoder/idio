const queryAPI = async (ep) => {
  document.getElementById('results').value = "Loading...";
  const response = await fetch(ep, {mode: 'no-cors'});
  const myJson = await response.json();
  document.getElementById('results').innerHTML = JSON.stringify(myJson).replace(/},{/g,"},<br/>&nbsp;<br/>{");
}

