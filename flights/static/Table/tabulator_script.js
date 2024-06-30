document.addEventListener('DOMContentLoaded', function () {

   
    // Funzione per ottenere l'URL basato sulle selezioni
    function getSelectedURL() {
        var mainCategory = $("#main-category").val();
        var subCategory = $("#sub-category").val();
        return `/${mainCategory}/${subCategory}`;
    }

    // Inizializzazione della tabella Tabulator
    var table = new Tabulator("#example-table", {
        ajaxURL: getSelectedURL(), // URL dinamico per il caricamento dei dati lato server
        ajaxParams: { page_size: 15 }, // Parametri per la richiesta AJAX
        pagination: "remote", // Paginazione lato server
        paginationSize: 15, // Numero di righe per pagina
        layout: "fitColumns", // Adatta le colonne alla larghezza della tabella
        placeholder: "Nessun dato disponibile", // Messaggio quando non ci sono dati
        columns: [], // Le colonne saranno determinate dinamicamente dopo il caricamento dei dati
        ajaxResponse: function (url, params, response) {
            // Aggiorna le colonne dinamicamente
            if (response.length > 0) {
                var columns = [];
                for (var key in response[0]) {
                    columns.push({ title: key.charAt(0).toUpperCase() + key.slice(1), field: key });
                }
                table.setColumns(columns);
            }
            return response;
        },
        ajaxSorting: true, // Abilita l'ordinamento AJAX
        ajaxFiltering: true, // Abilita il filtraggio AJAX
        selectable: true, // Abilita la selezione delle righe
        rowClick: function (e, row) {
            row.toggleSelect();
        }
    });

    // Event listener per il campo di ricerca
    // Aggiungi l'evento di input per il campo di ricerca
    $("#search").on("input", function () {
        var searchValue = $(this).val().toLowerCase();
        table.setFilter(customFilter);
    });

    // Definizione del filtro personalizzato
    function customFilter(data) {
        var searchValue = $("#search").val().toLowerCase();
        if (!searchValue) return true;

        // Controlla se uno qualsiasi dei valori della riga contiene il testo di ricerca
        for (var key in data) {
            if (data[key] && data[key].toString().toLowerCase().includes(searchValue)) {
                return true;
            }
        }
        return false;
    }

    // Cambia URL dinamicamente quando cambia la selezione delle categorie
    $("#main-category, #sub-category").on("change", function () {
        var selectedURL = getSelectedURL();
        table.setData(selectedURL);
    });

    // Gestione del pulsante Aggiungi riga
    $("#add-row").on("click", function () {
        openModal(null); // Passa null per indicare un nuovo inserimento
    });

    // Gestione del pulsante Modifica riga
    $("#edit-row").on("click", function () {
        var selectedData = table.getSelectedData();
        if (selectedData.length === 1) {
            openModal(selectedData[0]); // Passa i dati della riga selezionata per la modifica
        } else {
            showErrorModal("Seleziona una sola riga da modificare");
        }
    });

    // Gestione del pulsante Elimina riga
    $("#delete-row").on("click", function () {
        var mainCategory = $("#main-category").val();
        var selectedData = table.getSelectedData();
        if (selectedData.length > 0) {
            showDeleteConfirmation(function (confirmed) {
                if (confirmed) {
                    selectedData.forEach(function (row) {
                        // Chiamata AJAX per eliminare i dati
                        $.ajax({
                            url: mainCategory + "/delete/" + row.id,
                            type: 'DELETE',
                            method: 'POST',
                            success: function (result) {
                                table.setData(getSelectedURL());
                            },
                            error: function (xhr, status, error) {
                                showErrorModal("Errore durante l'eliminazione: " + error);
                            }
                        });
                    });
                }
            });
        } else {
            showErrorModal("Seleziona almeno una riga da eliminare");
        }
    });

    var modal = document.getElementById("data-modal");
    var span = document.getElementsByClassName("close")[0];

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Gestione del popup di conferma personalizzato
    function showDeleteConfirmation(callback) {
        var confirmModal = document.getElementById("confirm-modal");
        var confirmYes = document.getElementById("confirm-yes");
        var confirmNo = document.getElementById("confirm-no");
        var confirmMessage = document.getElementById("confirm-message");

        // Mostro il messaggio di conferma
        confirmMessage.textContent = "Sei sicuro di voler eliminare gli elementi selezionati?";
        confirmModal.style.display = "block";

        confirmYes.onclick = function () {
            confirmModal.style.display = "none";
            callback(true); // Conferma l'eliminazione
        };

        confirmNo.onclick = function () {
            confirmModal.style.display = "none";
            callback(false); // Annulla l'eliminazione
        };
    }

    // Funzione per mostrare un popup di errore
    function showErrorModal(message) {
        var errorModal = document.getElementById("error-modal");
        var errorMessage = document.getElementById("error-message");
        errorMessage.textContent = message;
        errorModal.style.display = "block";
    }

    // Inizializza il popup di errore
    var errorModal = document.getElementById("error-modal");
    var errorClose = document.getElementById("error-close");

    // Gestisce la chiusura del popup di errore
    errorClose.onclick = function () {
        errorModal.style.display = "none";
    };

    // Gestione del popup di modifica/inserimento dati
    var modal = document.getElementById("data-modal");
    var modalClose = document.getElementById("modal-close");

    // Gestisce la chiusura del popup di modifica/inserimento
    modalClose.onclick = function () {
        modal.style.display = "none";
    };

    // Gestione della chiusura del popup se si clicca al di fuori di esso
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        } else if (event.target == errorModal) {
            errorModal.style.display = "none";
        }
    };

    function openModal(data) {
        var mainCategory = $("#main-category").val();
        var form = document.getElementById("data-form");
        form.innerHTML = '';

        var url = (data === null) ? mainCategory + '/create' : mainCategory + '/update/' + data.id;
        var method = (data === null) ? 'POST' : 'POST';
    
        var columns = table.getColumnDefinitions();
        columns.forEach(function (col) {
            if (col.field !== "id") {
                var fieldDiv = document.createElement("div");
                var label = document.createElement("label");
                label.innerHTML = col.title;
                var input = document.createElement("input");
                input.type = "text";
                input.name = col.field;
                if (data) {
                    input.value = data[col.field] || "";
                }
                fieldDiv.appendChild(label);
                fieldDiv.appendChild(input);
                form.appendChild(fieldDiv);
            }
        });
    
        var saveButton = document.getElementById("submit-data");
        saveButton.onclick = function (event) {
            event.preventDefault();
    
            var formData = {};
            var formInputs = form.getElementsByTagName("input");
            for (var i = 0; i < formInputs.length; i++) {
                if (formInputs[i].type === 'text'|| formInputs[i].type === 'hidden') {
                    formData[formInputs[i].name] = formInputs[i].value;
                }
            }
            
            console.log(formData)

            $.ajax({
                url: url,
                type: method,
                data: formData,
                success: function (response) {
                    console.log("Dati salvati con successo:", response);
                    modal.style.display = "none";
                    table.setData(getSelectedURL());
                },
                error: function (xhr, status, error) {
                    showErrorModal("Errore durante il salvataggio: " + error);
                }
            });
        };

        modal.style.display = "block";
    }


});


