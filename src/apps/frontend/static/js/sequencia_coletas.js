// Constantes e variáveis globais
const BASE_URL = window.location.origin;
let currentPage = 1;
const itemsPerPage = 20;
let totalItems = 0;
const sequencias = `${BASE_URL}/api/v1/sequencias`;

const resultContainer = document.getElementById('result-list');
resultContainer.innerHTML = '';

// Função para fazer requisições JSON
async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Erro ao acessar a API: ${response.statusText}`);
    }
    return response.json();
}

// Função para criar um card
function createCard(item, edificacao, ponto) {
    const card = document.createElement('div');
    card.className = 'flex card';
    card.id = '' + item.id;

    card.innerHTML = `
        <button class="modal-button" onclick="change_modal_state(this)"><i class="bi bi-three-dots-vertical"></i></button>
        <div class="flex modal">
            <a href="" style="color: #525252;">Editar</a>
            <a href="" style="color: #FC1B44;">Remover</a>
        </div>
        <h6>${item.id}</h6>
        <h3>${edificacao.codigo}</h3>
        <h2>${edificacao.nome}</h2>
        <p>${item.tipo == 1 ? 'Bebedouro' : 'RPS'}</p>
        <p>${ponto.ambiente}</p>
        <h5>Amostragem ${item.amostragem}</h5>
        <button class="filled-button">
            <i class="bi bi-eye-fill"></i>
            Detalhes
        </button>
    `;
    resultContainer.appendChild(card);
}

// Função principal para buscar e exibir resultados
async function search(query = '') {
    try {
        const apiUrl = `${sequencias}?q=${encodeURIComponent(query)}`;
        const data = await fetchJson(apiUrl);

        const validItems = data.items.filter(item => item.ponto_url !== null);

        totalItems = validItems.length; 

        document.getElementById('page-info').textContent = `Página ${currentPage} de ${Math.ceil(totalItems / itemsPerPage)}`;
        updatePaginationButtons(); 

        resultContainer.innerHTML = '';

        const startIndex = (currentPage - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        validItems.slice(startIndex, endIndex).forEach(async (item) => {
            const pontoUrl = BASE_URL + item.ponto_url;
            const ponto = await fetchJson(pontoUrl);

            const edificacaoUrl = BASE_URL + ponto.edificacao_url;
            const edificacao = await fetchJson(edificacaoUrl);

            createCard(item, edificacao, ponto);
        });

    } catch (error) {
        console.error('Erro durante o processamento:', error);
    }
}

function handleQueryInput(event) {
    const query = event.target.value;
    currentPage = 1;
    search(query);
}

document.querySelector('input[name="search-query"]').addEventListener('input', handleQueryInput);

function goToPage(page) {
    currentPage = page;
    const query = document.querySelector('input[name="search-query"]').value;
    search(query);
}

function nextPage() {
    if ((currentPage * itemsPerPage) < totalItems) {
        goToPage(currentPage + 1);
    }
}

function prevPage() {
    if (currentPage > 1) {
        goToPage(currentPage - 1);
    }
}

document.getElementById('pagination-next').addEventListener('click', nextPage);
document.getElementById('pagination-prev').addEventListener('click', prevPage);

function updatePaginationButtons() {
    const prevButton = document.getElementById('pagination-prev');
    const nextButton = document.getElementById('pagination-next');

    prevButton.style.display = currentPage > 1 ? 'inline-block' : 'none';
    nextButton.style.display = (currentPage * itemsPerPage) < totalItems ? 'inline-block' : 'none';
}

search('');
