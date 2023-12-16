let isCriando = false;
let isAtualizando = false;
let isDeletando = false;

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

        sequencias.items.forEach(sequencia => {
            let newOption = document.createElement("option");
            newOption.value = `${sequencia.id}`;
            newOption.innerText = `Amostragem ${sequencia.amostragem}`;
            document.getElementById("sequencia").appendChild(newOption);

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

async function carregarColeta() {
    let target = window.location.pathname.split("/coletas/")[1];
    target = target.replace(/\/$/, "");

    try {
        const response = await fetch("/api/v1/coletas/" + target, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            window.location.href = "/coletas";
            return;
        }

        const data = await response.json();

        await fetchJson(data.sequencia_url)
            .then((sequencia) => {
                document.getElementById("sequencia_value").value = sequencia.amostragem;
            });

        await fetchJson(data.ponto_url)
            .then((ponto) => {
                document.getElementById("ponto_value").value = `${ponto.id} | ${ponto.ambiente} | ${ponto.tipo == '1' ? 'Bebedouro | ' + ponto.tombo : 'RPS'}`;
            });

        document.getElementById("temperatura").value = data.temperatura;
        document.getElementById("cloro").value = data.cloro_residual_livre;
        document.getElementById("turbidez").value = data.turbidez;
        document.getElementById("coliformes").checked = data.coliformes_totais;
        document.getElementById("escherichia").checked = data.escherichia;
        document.getElementById("cor").value = data.cor;
        document.getElementById("data").value = data.data.split("T")[0];
        document.getElementById("hora").value = data.data.split("T")[1].split(":00Z")[0];
        document.getElementById("ordem").value = data.ordem == "C" ? "Coleta" : "Recoleta";

        const responsaveisElement = document.querySelector("select[name='responsaveis']");
        if (responsaveisElement) {
            await fetchJson(data.responsaveis_url)
                .then((responsaveis) => {
                    responsaveis.forEach(responsavel => {
                        const option = responsaveisElement.querySelector(`option[value='${responsavel.id}']`);
                        if (option) {
                            option.selected = true;
                        }
                    });
                });
        }

        console.log("Coleta carregada com sucesso!");
    } catch (error) {
        console.error('Erro ao carregar coleta:', error);
    }
}

async function atualizarColeta() {
    
    if (isAtualizando) {
        return;
    }

    isAtualizando = true;

    const sequencia_id = document.getElementById("sequencia_value").value;
    const ponto_id = document.getElementById("ponto_value").value.split(" | ")[0];
    const temperatura = document.getElementById("temperatura").value;
    const cloro_residual_livre = document.getElementById("cloro").value;
    const turbidez = document.getElementById("turbidez").value;
    const coliformes_totais = document.getElementById("coliformes").checked;
    const escherichia = document.getElementById("escherichia").checked;
    const cor = document.getElementById("cor").value;
    let data = document.getElementById("data").value;
    const hora = document.getElementById("hora").value;
    const ordem = document.getElementById("ordem").value == "Coleta" ? "C" : "R";
    const responsaveis = document.getElementById("responsaveis").selectedOptions;

    const responsavel = []; // Array de ID dos responsáveis

    for (let i = 0; i < responsaveis.length; i++) {
        responsavel.push(responsaveis[i].value);
    }

    data = `${data}T${hora}:00Z`;
    
    const bt_atualizar = document.getElementById("atualizar");
    bt_atualizar.disabled = true;
    bt_atualizar.innerHTML = "Atualizando...";

    let target = window.location.pathname.split("/coletas/")[1];
    target = target.replace(/\/$/, "");

    try {
        
        const response = await fetch("/api/v1/coletas/" + target, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sequencia_id,
                ponto_id,
                temperatura,
                cloro_residual_livre,
                turbidez,
                coliformes_totais,
                escherichia,
                cor,
                data,
                ordem,
                responsavel
            }),
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(`Erro ao atualizar a coleta: ${response.statusText}. Detalhes: ${JSON.stringify(errorResponse)}`);
        }

        window.location.href = `/sequencias_coletas/${sequencia_id}`;

    } catch (error) {
        console.error('Erro ao atualizar a coleta:', error);
        bt_atualizar.disabled = false;
        bt_atualizar.innerHTML = "Atualizar";
    }
}

async function excluirColeta() {

    if (isDeletando) {
        return;
    }

    isDeletando = true;

    const bt_excluir = document.getElementById("excluir");
    bt_excluir.disabled = true;
    bt_excluir.innerHTML = "Excluindo...";

    let target = window.location.pathname.split("/coletas/")[1];
    target = target.replace(/\/$/, "");

    const sequencia_id = document.getElementById("sequencia_value").value;

    try {
        const response = await fetch("/api/v1/coletas/" + target, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(`Erro ao excluir a coleta: ${response.statusText}. Detalhes: ${JSON.stringify(errorResponse)}`);
        }

        window.location.href = `/sequencias_coletas/${sequencia_id}`;

    } catch (error) {
        console.error('Erro ao excluir a coleta:', error);
        bt_excluir.disabled = false;
        bt_excluir.innerHTML = "Excluir";
    }
}

// Adicionando um event listener aos botões
document.getElementById("atualizar").addEventListener("click", atualizarColeta);
document.getElementById("excluir").addEventListener("click", excluirColeta);


carregarOpcoesSequencia();
carregarOpcoesPonto();
carregarOpcoesResponsaveis();

carregarColeta();