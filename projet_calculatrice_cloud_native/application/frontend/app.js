const display = document.getElementById("display");
let openParenthesis = true;

// Ajouter une valeur au display
function appendToDisplay(value) {
  if (display.innerText === "0") {
    display.innerText = value;
  } else {
    display.innerText += value;
  }
}

// Ajouter ou fermer une parenthèse
function toggleParenthesis() {
  appendToDisplay(openParenthesis ? "(" : ")");
  openParenthesis = !openParenthesis;
}

// Effacer tout le display
function clearDisplay() {
  display.innerText = "0";
  openParenthesis = true;
}

// Supprimer le dernier caractère
function deleteLast() {
  let text = display.innerText;
  display.innerText = text.length > 1 ? text.slice(0, -1) : "0";
}

// Vérifier si le backend est en ligne
async function isBackendOnline() {
    try {
        const response = await fetch("http://127.0.0.1:5000/", { method: "GET" });
        console.log("Réponse du serveur : ", response.status);  // Log de réponse
        return response.ok;
    } catch (error) {
        console.error("Erreur réseau : ", error);  // Log des erreurs réseau
        return false;
    }
}


// Calculer le résultat en envoyant la requête au backend
async function calculateResult() {
  const backendOnline = await isBackendOnline();
  if (!backendOnline) {
    alert("Le serveur backend est hors ligne. Veuillez le démarrer.");
    display.innerText = "Erreur";
    return;
  }

  const expression = display.innerText;

  fetch("http://127.0.0.1:5000/calculate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ expression }), // Envoyer l'expression au backend
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Erreur du backend");
      }
      return response.json();
    })
    .then((data) => {
      if (data.error) {
        alert("Erreur: " + data.error);
        display.innerText = "Erreur";
      } else {
        display.innerText = data.result; // Afficher le résultat
      }
    })
    .catch((error) => {
      alert("Une erreur s'est produite : " + error.message);
      display.innerText = "Erreur";
    });
}
