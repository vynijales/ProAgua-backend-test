const BASE_URL = window.location.origin;
// const BASE_URL = "http://10.0.0.103:8000";

const sequencias = BASE_URL + "/api/v1/sequencias";

const resultContainer = document.getElementById('result-list');
resultContainer.innerHTML = '';

fetch(sequencias)
    .then((response) => {
        if (!response.ok) {
            throw new Error('Erro ao acessar a API: ' + response.statusText);
        }
        return response.json();
    })
    .then((data) => {
        const promises = data.items.map((item) => {
            if (item.ponto_url != null) {
                const pontoUrl = BASE_URL + item.ponto_url;
                const amostragem = item.amostragem
                return fetch(pontoUrl)
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error('Erro ao acessar a API de pontos: ' + response.statusText);
                        }
                        return response.json();
                    })
                    .then((ponto) => {
                        const edificacaoUrl = BASE_URL + ponto.edificacao_url;
                        return fetch(edificacaoUrl)
                            .then((response) => {
                                if (!response.ok) {
                                    throw new Error('Erro ao acessar a API de edificação: ' + response.statusText);
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
                                    <p>${ponto.ambiente}</p>
                                    <h5>Amostragem ${amostragem}</h5>
                                    <button class="filled-button">
                                        <i class="bi bi-eye-fill"></i>
                                        Detalhes
                                    </button>
                                `;
                                resultContainer.appendChild(card);
                            });
                    })
                    .catch((error) => {
                        console.error('Erro durante o processamento:', error);
                    });
            } else {
                console.log("Não tem ponto");
                return Promise.resolve();
            }
        });

        // Aguarda todas as promessas serem resolvidas antes de prosseguir
        return Promise.all(promises);
    })
    .catch((error) => {
        console.error('Erro durante a obtenção de sequências:', error);
    });