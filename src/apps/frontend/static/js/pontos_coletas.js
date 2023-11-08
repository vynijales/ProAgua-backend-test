
const BASE_URL = "http://10.0.0.103:8000";
const pontos = BASE_URL + "/api/v1/pontos";

function search(query) {
    const resultContainer = document.getElementById('result-list');
    resultContainer.innerHTML = '';

    fetch(pontos + `?q=${encodeURIComponent(query)}`)
        .then((response) => {
            if (!response.ok) {
                throw new Error('Erro ao acessar a API');
            }
            return response.json();
        })
        .then((data) => {
            data.items.forEach((item) => {
                const edificacao_url = BASE_URL + item.edificacao_url;

                fetch(edificacao_url)
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error('Erro ao acessar a URL da edificação');
                        }
                        return response.json();
                    })
                    .then((edificacao) => {
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
                        resultContainer.appendChild(card);
                    })
                    .catch((error) => {
                        console.error('Erro:', error);
                    });
            });
        })
        .catch((error) => {
            console.error('Erro:', error);
        });
}

document.querySelector('input[name="search-query"]').addEventListener('input', function (event) {
    const query = event.target.value;
    search(query);
});

search('');