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
    console.log("Réponse du serveur : ", response.status);
    return response.ok;
  } catch (error) {
    console.error("Erreur réseau : ", error);
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
        display.innerText = data.result;
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
