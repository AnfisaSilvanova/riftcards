document.addEventListener('DOMContentLoaded', () => {
    const detalheContainer = document.getElementById('detalhe-carta-container');

    // Pega o parâmetro 'id' da URL (ex: detalhe-carta.html?id=20)
    const params = new URLSearchParams(window.location.search);
    const cardId = params.get('id');

    // Se não houver ID na URL, exibe um erro
    if (!cardId) {
        detalheContainer.innerHTML = '<p style="color: #e94560;">ID da carta não fornecido na URL.</p>';
        return;
    }

    // Função para buscar os dados da carta específica
    async function carregarDetalhes() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/cards/${cardId}`);
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Erro HTTP: ${response.status}`);
            }
            const carta = await response.json();
            renderizarDetalhes(carta);

        } catch (error) {
            console.error("Falha ao buscar detalhes da carta:", error);
            detalheContainer.innerHTML = `<p style="color: #e94560;">Não foi possível carregar os detalhes. ${error.message}</p>`;
        }
    }

    // Função para construir o HTML com os detalhes da carta
    function renderizarDetalhes(carta) {
        detalheContainer.innerHTML = ''; // Limpa a mensagem de "carregando"

        const imgPath = `/static/assets/cards/${carta.img}`; // Ajuste o caminho se necessário

        const detalheElement = document.createElement('div');
        // A classe 'detalhe-container' já existe no seu CSS!
        detalheElement.classList.add('detalhe-container'); 
        detalheElement.innerHTML = `
            <div class="detalhe-imagem">
                <img src="${imgPath}" alt="${carta.name}">
            </div>
            <div class="detalhe-info">
                <h1>${carta.name}</h1>
                <h2 style="color: #ccc; font-style: italic;">${carta.subtitle || ''}</h2>
                <hr>
                <p><strong>Energia:</strong> ${carta.energy ?? 'N/A'}</p>
                <p><strong>Poder:</strong> ${carta.power ?? 'N/A'}</p>
                <p><strong>Força:</strong> ${carta.might ?? 'N/A'}</p>
                <hr>
                <h3>Habilidades</h3>
                <p>${carta.abilities || 'Nenhuma habilidade especial.'}</p>
                <hr>
                <p><em>"${carta.flavor || '...'}"</em></p>
            </div>
        `;

        detalheContainer.appendChild(detalheElement);
    }

    carregarDetalhes();
});