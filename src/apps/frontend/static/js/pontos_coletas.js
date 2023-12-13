// Constantes e variáveis globais
const BASE_URL = window.location.origin;
let currentPage = 1;
const itemsPerPage = 24;
let totalItems = 0;
const pontos = `${BASE_URL}/api/v1/pontos`;

// Função para fazer requisições JSON
async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Erro ao acessar a API: ${response.statusText}`);
    }
    return response.json();
}

// Função para criar um card
function createCard(item, edificacao) {
    const card = document.createElement('div');
    card.className = 'flex card';
    
    card.id = '' + item.id;

    card.innerHTML = `
    <a class="modal-button" href= "/pontos/${item.id}"><i class="bi bi-pencil-square"></i></a>        <h3>${edificacao.codigo}</h3>
        <h2>${edificacao.nome}</h2>
        <p>${item.tipo == 1 ? 'Bebedouro' : 'RPS'}</p>
        <p>${item.ambiente}</p>
        <button class="filled-button">
            <i class="bi bi-eye-fill"></i>
            Detalhes
        </button>
    `;
    return card;
}

// Função para atualizar a visibilidade dos botões de navegação
function updatePaginationButtons() {
    const prevButton = document.getElementById('pagination-prev');
    const nextButton = document.getElementById('pagination-next');

    prevButton.style.display = currentPage > 1 ? 'inline-block' : 'none';
    nextButton.style.display = (currentPage * itemsPerPage) < totalItems ? 'inline-block' : 'none';
}

// Função principal para buscar e exibir resultados
async function search(query, campus, page = 1) {
    const resultContainer = document.getElementById('result-list');
    resultContainer.innerHTML = '';

    try {
        
        const campusQueryParam = campus ? `&campus=${encodeURIComponent(campus)}` : '';
        const pageQueryParam = `&limit=${itemsPerPage}&offset=${(page - 1) * itemsPerPage}`;
        const apiUrl = `${pontos}?q=${encodeURIComponent(query)}${campusQueryParam}${pageQueryParam}`;

        console.log('API URL:', apiUrl); // Adicione esta linha para depuração

        const data = await fetchJson(apiUrl);

        if (data && data.items) {
            totalItems = data.count;

            const edificacoes = await Promise.all(data.items.map(item => fetchJson(`${BASE_URL}${item.edificacao_url}`)));

            data.items.forEach((item, index) => {
                const edificacao = edificacoes[index];
                const card = createCard(item, edificacao);
                resultContainer.appendChild(card);
            });
        } else {
            console.error('Data ou data.items não encontrados');
        }

        // Atualizar a informação da página
        document.getElementById('page-info').textContent = `Página ${currentPage} de ${Math.ceil(totalItems / itemsPerPage)}`;
        updatePaginationButtons();

    } catch (error) {
        console.error('Erro:', error);
    }
}


// Função para lidar com a mudança do seletor campus
function handleCampusChange(event) {
    const query = document.querySelector('input[name="search-query"]').value;
    const campus = event.target.value;
    currentPage = 1;
    search(query, campus);
}

// Função para lidar com a entrada do input search
function handleQueryInput(event) {
    const query = event.target.value;
    const campus = document.querySelector('select[name="campus"]').value;
    currentPage = 1;
    search(query, campus);
}

// Função para ir para uma página específica
function goToPage(page) {
    currentPage = page;
    const query = document.querySelector('input[name="search-query"]').value;
    const campus = document.querySelector('select[name="campus"]').value;
    search(query, campus, currentPage);
}

// Função para ir para a próxima página
function nextPage() {
    if ((currentPage * itemsPerPage) < totalItems) {
        goToPage(currentPage + 1);
    }
}

// Função para ir para a página anterior
function prevPage() {
    if (currentPage > 1) {
        goToPage(currentPage - 1);
    }
}

// Adicionar ouvintes de eventos
document.querySelector('select[name="campus"]').addEventListener('change', handleCampusChange);
document.querySelector('input[name="search-query"]').addEventListener('input', handleQueryInput);
document.getElementById('pagination-next').addEventListener('click', nextPage);
document.getElementById('pagination-prev').addEventListener('click', prevPage);

// Inicializar a pesquisa com valores padrão
search('', '');

// Exibir mensagem de log no console
console.log('Pontos de coleta carregados');
