document.addEventListener('DOMContentLoaded', () => {
    // --- Lógica do Montador de Decks ---
    const deckList = document.getElementById('deck-list');
    const cardCount = document.getElementById('card-count');
    const addCardButtons = document.querySelectorAll('.btn-add');
    const clearDeckButton = document.getElementById('clear-deck');

    let currentDeck = [];

    // Função para renderizar o deck
    const renderDeck = () => {
        if (!deckList) return; // Só executa na página do builder
        
        deckList.innerHTML = ''; // Limpa a lista antes de renderizar
        currentDeck.forEach(cardName => {
            const cardElement = document.createElement('div');
            cardElement.classList.add('deck-list-card');
            cardElement.innerHTML = `
                <span>${cardName}</span>
                <button class="btn-remove" data-name="${cardName}">&times;</button>
            `;
            deckList.appendChild(cardElement);
        });
        
        // Atualiza a contagem de cartas
        cardCount.textContent = currentDeck.length;
        
        // Adiciona event listener aos novos botões de remoção
        addRemoveListeners();
    };
    
    // Adiciona uma carta ao deck
    addCardButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            if (currentDeck.length >= 30) {
                alert("O deck já está cheio (30 cartas)!");
                return;
            }
            const cardName = e.target.closest('.card-builder-item').dataset.name;
            currentDeck.push(cardName);
            renderDeck();
        });
    });

    // Função para adicionar listeners aos botões de remoção
    const addRemoveListeners = () => {
        document.querySelectorAll('.btn-remove').forEach(button => {
            button.addEventListener('click', (e) => {
                const cardNameToRemove = e.target.dataset.name;
                const cardIndex = currentDeck.indexOf(cardNameToRemove);
                if (cardIndex > -1) {
                    currentDeck.splice(cardIndex, 1);
                }
                renderDeck();
            });
        });
    };

    // Limpa o deck
    if(clearDeckButton) {
        clearDeckButton.addEventListener('click', () => {
            currentDeck = [];
            renderDeck();
        });
    }
});