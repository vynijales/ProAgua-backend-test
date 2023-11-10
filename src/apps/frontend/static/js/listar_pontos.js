const BASE_URL = window.location.origin;
const pontos = BASE_URL + "/api/v1/pontos"

function search(query) {
    const resultsTable = document.getElementById('table-body');
    resultsTable.innerHTML = '';

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
                        const row = resultsTable.insertRow();

                        const cell1 = row.insertCell();
                        const cell2 = row.insertCell();
                        const cell3 = row.insertCell();
                        const cell4 = row.insertCell();
                        const cell5 = row.insertCell();
                        const cell6 = row.insertCell();

                        cell1.innerHTML = edificacao.codigo;
                        cell2.innerHTML = edificacao.nome;
                        cell3.innerHTML = edificacao.campus;
                        cell4.innerHTML = item.ambiente;
                        cell5.innerHTML = item.tipo == 1 ? "Bebedouro" : "Torneira";
                        cell6.innerHTML = item.tombo;
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