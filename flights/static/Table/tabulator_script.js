document.addEventListener('DOMContentLoaded', function () {
    // Funzione per ottenere l'URL basato sulle selezioni
    function getSelectedURL() {
        var mainCategory = document.getElementById('main-category').dataset.value;
        var subCategory = document.getElementById('sub-category').getAttribute('data-value');

        // Impostiamo valori di default se mainCategory o subCategory sono undefined
        if (!mainCategory) {
            mainCategory = 'airlines'; // Imposta il default su 'airlines'
        }
        if (!subCategory) {
            subCategory = 'getAll'; // Imposta il default su 'getAll'
        }

        return `/${mainCategory}/${subCategory}`;
    }

    // Mappa per convertire i nomi delle funzioni in nomi visualizzati
    var functionToDisplayName = {
        'getAll': 'GetAll',
        'getAirlineForCountry/<str:country>': 'GetAirlineForCountry',
        'getActiveAirlines': 'GetActiveAirlines',
        'matching_codes': 'Matching Codes',
        'airports_by_country': 'Airports By Country',
        'get_cities_with_most_airports': 'Cities with Most Airports',
        'statistics_routes': 'Statistics',
        'max_stops': 'Max Stops'
    };

    // Funzione per aggiornare il dropdown delle subcategorie
    function updateSubCategoryDropdown(mainCategory) {
        var subCategoryDropdown = document.getElementById('sub-category-dropdown');
        var subCategoryOptions = subCategoryDropdown.querySelector('.option');
        subCategoryOptions.innerHTML = '';
        $.ajax({
            url: '/get_subcategories/',
            method: 'GET',
            data: { main_category: mainCategory },
            success: function (data) {
                data.forEach(function (item) {
                    var displayName = functionToDisplayName[item] || item;
                    var option = document.createElement('div');
                    option.setAttribute('data-value', item);
                    option.innerHTML = `<ion-icon name="stats-chart"></ion-icon> ${displayName}`;
                    subCategoryOptions.appendChild(option);

                    option.addEventListener('click', function() {
                        var input = subCategoryDropdown.querySelector('.textBox');
                        input.value = this.textContent.trim();
                        input.setAttribute('data-value', this.getAttribute('data-value'));
                        subCategoryDropdown.classList.remove('active');
                        subCategoryOptions.style.display = 'none';

                        table.setData(getSelectedURL());
                    });
                });

                var subCategoryInput = subCategoryDropdown.querySelector('.textBox');
                subCategoryInput.value = 'GetAll';
                subCategoryInput.setAttribute('data-value', 'getAll');
            },
            error: function (xhr, status, error) {
                showErrorModal("Errore durante il caricamento dei sub-category: " + error);
            }
        });
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

    // Gestione dei dropdown personalizzati
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        const input = dropdown.querySelector('.textBox');
        const options = dropdown.querySelector('.option');

        input.addEventListener('click', function() {
            dropdown.classList.toggle('active');
            options.style.display = dropdown.classList.contains('active') ? 'block' : 'none';
        });

        options.querySelectorAll('div[data-value]').forEach(option => {
            option.addEventListener('click', function() {
                input.value = this.textContent.trim();
                input.setAttribute('data-value', this.getAttribute('data-value'));
                dropdown.classList.remove('active');
                options.style.display = 'none';
                var mainCategory = document.getElementById('main-category').getAttribute('data-value');

                // Prima di aggiornare le subcategorie, resetta il sub-category a 'GetAll'
                var subCategoryInput = document.getElementById('sub-category');
                subCategoryInput.setAttribute('data-value', 'getAll');
                subCategoryInput.value = 'GetAll';

                updateSubCategoryDropdown(mainCategory);

                // Aggiorna la tabella solo dopo che il sub-category è stato aggiornato
                setTimeout(function () {
                    table.setData(getSelectedURL());
                }, 100); // Imposta un piccolo ritardo per garantire l'aggiornamento del sub-category
            });
        });
    });

    // Chiama updateSubCategoryDropdown all'inizializzazione della pagina
    var mainCategory = document.getElementById('main-category').dataset.value || 'airlines';
    updateSubCategoryDropdown(mainCategory);

    // Cambia URL dinamicamente quando cambia la selezione delle categorie
    document.querySelectorAll('.textBox').forEach(input => {
        input.addEventListener('change', function () {
            var selectedURL = getSelectedURL();
            table.setData(selectedURL);
        });
    });

    table.on("tableBuilt", function() {
        var footerDiv = document.querySelector('.tabulator-footer');

        if (footerDiv) {
            // Creare un nuovo div per contenere i bottoni e la ricerca
            var buttonContainerDiv = document.createElement('div');
            buttonContainerDiv.className = 'button-container';

            // Sposta i bottoni nel nuovo div
            var addButton = document.getElementById('add-row');
            var editButton = document.getElementById('edit-row');
            var deleteButton = document.getElementById('delete-row');

            buttonContainerDiv.appendChild(addButton);
            buttonContainerDiv.appendChild(editButton);
            buttonContainerDiv.appendChild(deleteButton);

            // Crea un div per la barra di ricerca
            var searchContainerDiv = document.createElement('div');
            searchContainerDiv.className = 'search-container';

            var search = document.getElementById('search');
            searchContainerDiv.appendChild(search);
            var cercaButton = document.getElementById('Cerca');
            searchContainerDiv.appendChild(cercaButton);

            // Crea un div per il paginator
            var paginatorContainerDiv = document.createElement('div');
            paginatorContainerDiv.className = 'paginator-container';

            // Inserisce il paginator originale nel nuovo div
            while (footerDiv.firstChild) {
                paginatorContainerDiv.appendChild(footerDiv.firstChild);
            }

            // Aggiungi i nuovi div nel footerDiv
            footerDiv.appendChild(buttonContainerDiv);
            footerDiv.appendChild(searchContainerDiv);
            footerDiv.appendChild(paginatorContainerDiv);
        } else {
            console.error('Div with class "tabulator-footer" not found.');
        }
    });

    // Event listener per il campo di ricerca
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

    // Gestione del pulsante Elimina riga
    $("#delete-row").on("click", function () {
        var mainCategory = document.getElementById('main-category').dataset.value;
        if (!mainCategory) {
            mainCategory = 'airlines'; // Imposta il default su 'airlines'
        }
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

    // Event listener per il pulsante Aggiungi riga
    $("#add-row").on("click", function () {
        openModal(null); // Passa null per indicare che è una nuova riga
    });

    // Event listener per il pulsante Modifica riga
    $("#edit-row").on("click", function () {
        var selectedData = table.getSelectedData();
        if (selectedData.length === 1) {
            openModal(selectedData[0]); // Passa i dati della riga selezionata per la modifica
        } else {
            showErrorModal("Seleziona una riga per modificare");
        }
    });

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

    // Funzione per mostrare un popup di conferma personalizzato
    function showDeleteConfirmation(callback) {
        var confirmModal = document.getElementById("confirm-modal");
        var confirmYes = document.getElementById("confirm-yes");
        var confirmNo = document.getElementById("confirm-no");
        var confirmMessage = document.getElementById("confirm-message");

        // Mostra il messaggio di conferma
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

    // Funzione per aprire il popup di modifica/inserimento dati

    function validateInput(input) {
        var isValid = true;

        // Controlla se l'input è di tipo testo o nascosto
        if (input.type === 'text' || input.type === 'hidden') {
            // Se il valore dell'input è vuoto, aggiungi la classe 'invalid-input' e imposta il flag di validazione a false
            if (input.value.trim() === "") {
                input.classList.add('invalid-input');
                isValid = false;
            } else {
                // Se il valore dell'input non è vuoto, rimuovi la classe 'invalid-input'
                input.classList.remove('invalid-input');
            }
        }

        return isValid; // Ritorna il flag di validazione
    }


    function openModal(data) {
        var mainCategory = document.getElementById('main-category').dataset.value;
        var form = document.getElementById("data-form");

        if (!mainCategory) {
            mainCategory = 'airlines'; // Imposta il default su 'airlines'
        }

        form.innerHTML = '';

        var url = (data === null) ? mainCategory + '/create' : mainCategory + '/update/' + data.id;
        var method = (data === null) ? 'POST' : 'POST';

        var columns = table.getColumnDefinitions();
        columns.forEach(function (col) {
            if (col.field !== "id") {
                var fieldDiv = document.createElement("div");
                fieldDiv.className = "field-div"; // Aggiungi la classe qui

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

            var isValid = true; // Flag per verificare la validità del form
            var formData = new FormData(); // Utilizza un oggetto FormData per raccogliere i dati

            var formInputs = form.getElementsByTagName("input");

            // Validazione di tutti gli input del form e aggiunta dei dati a formData
            for (var i = 0; i < formInputs.length; i++) {
                if (!validateInput(formInputs[i])) {
                    isValid = false;
                }
                formData.append(formInputs[i].name, formInputs[i].value);
            }

            // Se il form non è valido, non inviare i dati
            if (!isValid) {
                showErrorModal("Compila correttamente tutti i campi evidenziati.");
                return;
            }

            // Se il form è valido, invia i dati con AJAX
            $.ajax({
                url: url,
                type: method,
                data: formData, // Invia l'oggetto FormData
                processData: false, // Evita che jQuery elabori i dati
                contentType: false, // Imposta il tipo di contenuto su false
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


        // Rimuovi eventuali altezze preimpostate
        var modalContent = document.querySelector('.modal-content');
        modalContent.style.height = 'auto';

        // Visualizza la modale
        modal.style.display = "block";

        // Calcola l'altezza del contenuto
        var contentHeight = modalContent.scrollHeight;

        // Imposta l'altezza della modale in base al contenuto
        modalContent.style.height = contentHeight + 'px';
    }

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

});
