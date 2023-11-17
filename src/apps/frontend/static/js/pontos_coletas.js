const BASE_URL = window.location.origin;
// const BASE_URL = "https://10.0.0.103:8000";
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

async function search(query, campus) {
    const resultContainer = document.getElementById('result-list');
    resultContainer.innerHTML = '';

    try {
        const campusQueryParam = campus ? `&campus=${encodeURIComponent(campus)}` : '';
        const data = await fetchJson(`${pontos}?q=${encodeURIComponent(query)}${campusQueryParam}`);

        if (data && data.items) {
            const edificacoes = await Promise.all(data.items.map(item => fetchJson(BASE_URL + item.edificacao_url)));

            data.items.forEach((item, index) => {
                const edificacao = edificacoes[index];
                const card = createCard(item, edificacao);
                resultContainer.appendChild(card);
            });
        } else {
            console.error('Data or data.items is undefined.');
        }
    } catch (error) {
        console.error('Erro:', error);
    }
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

console.log('Pontos de coleta carregados');
