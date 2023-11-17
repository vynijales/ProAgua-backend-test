const BASE_URL = window.location.origin;
const pontos = BASE_URL + "/api/v1/pontos";

function fetchJson(url) {
    return fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Erro ao acessar a API: ${response.statusText}`);
            }
            return response.json();
        });
}

function createCard(item, edificacao) {
    const card = document.createElement('div');
    card.className = 'flex card';
    
    card.id = '' + item.id;

    card.innerHTML = `
        <button class="modal-button" onclick="change_modal_state(this)"><i class="bi bi-three-dots-vertical"></i></button>
        <div class="flex modal">
            <a href="" style="color: #525252;">Editar</a>
            <a href="" style="color: #FC1B44;">Remover</a>
        </div>
        <h3>${edificacao.codigo}</h3>
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

function search(query, campus) {
    const resultContainer = document.getElementById('result-list');
    resultContainer.innerHTML = '';

    const campusQueryParam = campus ? `&campus=${encodeURIComponent(campus)}` : '';
    
    fetchJson(`${pontos}?q=${encodeURIComponent(query)}${campusQueryParam}`)
        .then((data) => {
            const edificacaoPromises = data.items.map((item) => {
                const edificacao_url = BASE_URL + item.edificacao_url;
                return fetchJson(edificacao_url);
            });

            return Promise.all(edificacaoPromises);
        })
        .then((edificacoes) => {
            data.items.forEach((item, index) => {
                const edificacao = edificacoes[index];
                const card = createCard(item, edificacao);
                resultContainer.appendChild(card);
            });
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
}

function handleCampusChange(event) {
    const query = document.querySelector('input[name="search-query"]').value;
    const campus = event.target.value;
    search(query, campus);
}

function handleQueryInput(event) {
    const query = event.target.value;
    const campus = document.querySelector('select[name="campus"]').value;
    search(query, campus);
}

document.querySelector('select[name="campus"]').addEventListener('change', handleCampusChange);
document.querySelector('input[name="search-query"]').addEventListener('input', handleQueryInput);

search('', '');
