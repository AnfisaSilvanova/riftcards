document.addEventListener('DOMContentLoaded', () => {
    const catalogoGrid = document.querySelector('.catalogo-grid');

    // --- Seletores para os filtros ---
    const rarityFilter = document.getElementById('rarity-filter');
    const keywordFilter = document.getElementById('keyword-filter');
    const energySlider = document.getElementById('energy-slider');
    const energyValueSpan = document.getElementById('energy-value');

    // --- Função Principal para Buscar e Renderizar ---
    async function fetchAndRenderCards() {
        // Constrói a URL com os parâmetros de filtro
        const queryParams = getQueryParameters();
        const url = `http://127.0.0.1:5000/api/cards?${queryParams}`;

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);
            
            const cartas = await response.json();
            renderizarCartas(cartas);

        } catch (error) {
            console.error("Falha ao buscar cartas:", error);
            catalogoGrid.innerHTML = '<p style="color: #e94560;">Não foi possível carregar as cartas.</p>';
        }
    }

    // --- Função para ler os filtros e criar a query string ---
    function getQueryParameters() {
        const params = new URLSearchParams();

        // Obtém raridades selecionadas
        const selectedRarities = Array.from(rarityFilter.querySelectorAll('input:checked'))
            .map(input => input.value);
        if (selectedRarities.length > 0) {
            params.append('rarities', selectedRarities.join(','));
        }

        // Obtém keywords selecionadas
        const selectedKeywords = Array.from(keywordFilter.querySelectorAll('input:checked'))
            .map(input => input.value);
        if (selectedKeywords.length > 0) {
            params.append('keywords', selectedKeywords.join(','));
        }

        

        // Obtém valor do custo de energia (só adiciona se não for o máximo)
        if (energySlider.value < 10) {
            params.append('max_energy', energySlider.value);
        }

        return params.toString();
    }

    // --- Função para renderizar as cartas na tela (igual a antes) ---
    function renderizarCartas(cartas) {
        catalogoGrid.innerHTML = ''; 
        if (cartas.length === 0) {
            catalogoGrid.innerHTML = '<p>Nenhuma carta encontrada com os filtros selecionados.</p>';
            return;
        }
        cartas.forEach(carta => {
            const cardElement = document.createElement('div');
            cardElement.classList.add('card-anuncio');
            const imageName = carta.img ? carta.img.trim() : '';
            const imgPath = `/static/assets/cards/${imageName}`;
            cardElement.innerHTML = `
                <img src="${imgPath}" alt="${carta.name}" onerror="this.style.display='none';">
                <h3>${carta.name}</h3>
                <a href="detalhe-carta.html?id=${carta.id}">Ver Detalhes</a>
            `;
            catalogoGrid.appendChild(cardElement);
        });
    }
    
    // --- Adiciona os Event Listeners ---
    // 'change' é acionado quando uma checkbox é marcada/desmarcada
    rarityFilter.addEventListener('change', fetchAndRenderCards);
    keywordFilter.addEventListener('change', fetchAndRenderCards);
    
    // 'input' é acionado continuamente enquanto o slider é movido
    energySlider.addEventListener('input', () => {
        const value = energySlider.value;
        energyValueSpan.textContent = value == 10 ? `Custo: 10 ou menos` : `Custo: ${value} ou menos`;
        fetchAndRenderCards(); // Busca novamente ao mover o slider
    });


    // --- Carregamento Inicial ---
    // Inicia o carregamento das cartas quando a página abre
    fetchAndRenderCards();
});