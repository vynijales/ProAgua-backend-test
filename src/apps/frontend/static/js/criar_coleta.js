async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Erro ao acessar a API: ${response.statusText}`);
    }
    return response.json();
}

async function carregarOpcoesPonto() {
    try {
        const pontos = await fetchJson("/api/v1/pontos");
        const pontoInput = document.querySelector("input[name='ponto']");

        pontoInput.innerHTML = "";

        pontos.items.forEach(ponto => {
            let newOption = document.createElement("option");
            newOption.id = ponto.id;
            newOption.value = `${ponto.id} - ${ponto.ambiente} | ${ponto.tipo == '1' ? 'Bebedouro | ' + ponto.tombo : 'RPS'}`;
            document.getElementById("ponto").appendChild(newOption);
        });

    } catch (error) {
        console.error('Erro ao carregar opções de coleta:', error);
    }
}

async function carregarOpcoesResponsaveis() {
    try {
        const responsaveis = await fetchJson("/api/v1/usuarios");
        const responsavelSelect = document.querySelector("select[name='responsaveis']");

        responsavelSelect.innerHTML = "";

        console.log(responsaveis);
        responsaveis.items.forEach(responsavel => {
            let newOption = document.createElement("option");
            newOption.id = responsavel.id;
            newOption.innerText = responsavel.username;
            document.getElementById("responsaveis").appendChild(newOption);
        });

    } catch (error) {
        console.error('Erro ao carregar opções de responsáveis:', error);
    }
}

carregarOpcoesPonto();
carregarOpcoesResponsaveis();