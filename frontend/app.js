fetch("/api/clients")
  .then(response => response.json())
  .then(data => {
    document.getElementById("output").innerText =
      JSON.stringify(data, null, 2);
  })
  .catch(() => {
    document.getElementById("output").innerText =
      "Erreur lors de l'appel API";
  });
