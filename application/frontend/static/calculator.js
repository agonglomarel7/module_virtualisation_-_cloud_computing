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
<<<<<<< HEAD:projet_calculatrice_cloud_native/application/frontend/app.js
  try {
    const response = await fetch("http://127.0.0.1:5000/", { method: "GET" });
    console.log("Réponse du serveur : ", response.status);
    return response.ok;
  } catch (error) {
    console.error("Erreur réseau : ", error);
    return false;
  }
}

=======
    try {
        const response = await fetch(`${window.BACKEND_URL}`, { method: "GET" });
        console.log("Réponse du serveur : ", response.status);  // Log de réponse
        return response.ok;
    } catch (error) {
        console.error("Erreur réseau : ", error);  // Log des erreurs réseau
        return false;
    }
}

async function getResult(operationId) {
  try {
    const response = await fetch(`${window.BACKEND_URL}/result/${operationId}`);
    
    if (!response.ok) {
      throw new Error("Erreur lors de la récupération du résultat");
    }

    const data = await response.json();

    if (data.error) {
      alert("Erreur: " + data.error);
      display.innerText = "Erreur";
    } else if (data.result === "pending") {
      alert("Le résultat n'est pas encore prêt, réessayez plus tard.");
      display.innerText = "En attente";
      // Vous pouvez relancer la fonction après un délai pour vérifier à nouveau
      setTimeout(() => getResult(operationId), 2000); // Vérifier toutes les 2 secondes
    } else {
      console.log("Résultat reçu : ", data.result);
      display.innerText = data.result;
    }
  } catch (error) {
    alert("Une erreur s'est produite lors de la récupération du résultat : " + error.message);
    display.innerText = "Erreur";
  }
}


>>>>>>> 516159b94cc84d89567f5c1c5fe41461e17ed85d:application/frontend/static/calculator.js
// Calculer le résultat en envoyant la requête au backend
async function calculateResult() {
  const backendOnline = await isBackendOnline();
  if (!backendOnline) {
    alert("Le serveur backend est hors ligne. Veuillez le démarrer.");
    display.innerText = "Erreur";
    return;
  }

  const expression = display.innerText;

  fetch(`${window.BACKEND_URL}/calculate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ expression }), 
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
<<<<<<< HEAD:projet_calculatrice_cloud_native/application/frontend/app.js
        display.innerText = data.result;
=======
        console.log("ID de l'opération : ", data.id);
        // Appeler la fonction pour obtenir le résultat
        getResult(data.id);  // Utiliser l'ID pour récupérer le résultat
>>>>>>> 516159b94cc84d89567f5c1c5fe41461e17ed85d:application/frontend/static/calculator.js
      }
    })
    .catch((error) => {
      alert("Une erreur s'est produite : " + error.message);
      display.innerText = "Erreur";
    });
}

// Fonctions scientifiques
function square() {
  display.innerText += "**2"; 
}

function cube() {
  display.innerText += "**3"; 
}

function sqrt() {
  display.innerText = `sqrt(${display.innerText})`;
}

function cbrt() {
  display.innerText = `cbrt(${display.innerText})`;
}

function factorial() {
  display.innerText = `fact(${display.innerText})`;
}

function sin() {
  display.innerText = `sin(${display.innerText})`;
}

function cos() {
  display.innerText = `cos(${display.innerText})`;
}

function tan() {
  display.innerText = `tan(${display.innerText})`;
}
