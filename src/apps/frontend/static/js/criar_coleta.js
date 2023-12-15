let isCriando = false;

async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Erro ao acessar a API: ${response.statusText}`);
    }
    return response.json();
}

async function carregarOpcoesSequencia() {
    try {
        const sequencias = await fetchJson("/api/v1/sequencias");
        const sequenciaInput = document.querySelector("input[name='sequencia']");

        sequenciaInput.innerHTML = "";

        console.log(sequencias)
        sequencias.items.forEach(sequencia => {
            let newOption = document.createElement("option");
            newOption.value = `${sequencia.id}`;
            newOption.innerText = `Amostragem ${sequencia.amostragem}`;
            document.getElementById("sequencia").appendChild(newOption);

            console.log(sequencia);
        });

    } catch (error) {
        console.error('Erro ao carregar opções de edificação:', error);
    }
}


async function carregarOpcoesPonto() {
    try {
        const pontos = await fetchJson("/api/v1/pontos");
        const pontoInput = document.querySelector("input[name='ponto']");

        pontoInput.innerHTML = "";

        pontos.items.forEach(ponto => {
            let newOption = document.createElement("option");
            newOption.value = `${ponto.id} | ${ponto.ambiente} | ${ponto.tipo == '1' ? 'Bebedouro | ' + ponto.tombo : 'RPS'}`;
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

        responsaveis.items.forEach(responsavel => {
            let newOption = document.createElement("option");
            newOption.value = responsavel.id;
            newOption.innerText = responsavel.username;
            document.getElementById("responsaveis").appendChild(newOption);
        });

    } catch (error) {
        console.error('Erro ao carregar opções de responsáveis:', error);
    }
}

async function criarColeta() {
    if (isCriando) {
        console.log("Já existe uma requisição em andamento");
        return;
    }

    isCriando = true;
    const bt_criar = document.getElementById("criar");
    bt_criar.disabled = true;
    bt_criar.innerHTML = "Criando...";

    const sequencia = document.getElementById("sequencia_value").value;
    const ponto_coleta = document.getElementById("ponto_value").value;
    const ponto_coleta_id = parseInt(ponto_coleta.split(" | ")[0]);
    const temperatura = document.getElementById("temperatura").value;
    const cloro = document.getElementById("cloro").value;
    const turbidez = document.getElementById("turbidez").value;
    const coliformes = document.getElementById("coliformes").checked;
    const escherichia = document.getElementById("escherichia").checked;
    const cor = document.getElementById("cor").value;
    const data = document.getElementById("data").value;
    const hora = document.getElementById("hora").value;
    const responsaveis = [];
    document.querySelectorAll("select[name='responsaveis'] option:checked").forEach(option => responsaveis.push(option.value));

    const ordem = document.getElementById("ordem").value;

    const json = {
        "sequencia_id": sequencia,
        "ponto_id": ponto_coleta_id,
        "temperatura": temperatura,
        "cloro_residual_livre": cloro,
        "turbidez": turbidez,
        "coliformes_totais": coliformes,
        "escherichia": escherichia,
        "cor": cor,
        "data": data + "T" + hora + ":00Z",
        "responsavel": responsaveis,
        "ordem": ordem
    };

    const responseColeta = await fetch("/api/v1/coletas/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(json),
    });

    if (!responseColeta.ok) {
        const errorResponse = await responseColeta.json();
        throw new Error(`Erro ao criar a coleta: ${responseColeta.statusText}. Detalhes: ${JSON.stringify(errorResponse)}`);
    }

    window.location.href = `/sequencias_coletas/${sequencia}`;
    console.log("Coleta criada com sucesso!");


    isCriando = false;
    bt_criar.disabled = false;
    bt_criar.innerHTML = "Criar";
}

// Adicionando um event listener ao botão
document.getElementById("criar").addEventListener("click", criarColeta);


carregarOpcoesSequencia();
carregarOpcoesPonto();
carregarOpcoesResponsaveis();