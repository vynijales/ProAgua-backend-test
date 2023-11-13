const BASE_URL = window.location.origin;
const pontos = BASE_URL + "/api/v1/pontos";

function search(query, campus) {
    const resultContainer = document.getElementById('result-list');
    resultContainer.innerHTML = '';

    const campusQueryParam = campus ? `&campus=${encodeURIComponent(campus)}` : '';
    fetch(`${pontos}?q=${encodeURIComponent(query)}${campusQueryParam}`)
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

document.querySelector('select[name="campus"]').addEventListener('change', function (event) {
    const query = document.querySelector('input[name="search-query"]').value;
    const campus = event.target.value;
    search(query, campus);
});

document.querySelector('input[name="search-query"]').addEventListener('input', function (event) {
    const query = event.target.value;
    const campus = document.querySelector('select[name="campus"]').value;
    search(query, campus);
});

search('', '');