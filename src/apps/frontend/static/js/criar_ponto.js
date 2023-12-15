let isCriando = false;

async function fetchJson(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`Erro ao acessar a API: ${response.statusText}`);
    }
    return response.json();
}

async function carregarOpcoesEdificacao() {
    try {
        const edificacoes = await fetchJson("/api/v1/edificacoes");
        const edificacaoInput = document.querySelector("input[name='edificacao']");

        edificacaoInput.innerHTML = "";

        edificacoes.items.forEach(edificacao => {
            let newOption = document.createElement("option");
            newOption.value = edificacao.codigo;
            document.getElementById("edificacao").appendChild(newOption);
        });

    } catch (error) {
        console.error('Erro ao carregar opções de edificação:', error);
    }
}

function atualizarPreview() {
    const inputFoto = document.getElementById("foto");
    const imgElement = document.getElementById("imagePreview");

    if (inputFoto.files && inputFoto.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            imgElement.src = e.target.result;
        };

        reader.readAsDataURL(inputFoto.files[0]);
    }
}

async function criarPonto() {
    if (isCriando) {
        console.log("Já existe uma requisição em andamento");
        return;
    }

    isCriando = true;
    const bt_criar = document.getElementById("criar");
    bt_criar.disabled = true;
    bt_criar.innerHTML = "Criando...";

    try {
        const ambiente = document.getElementById("ambiente").value;
        const tipo = document.getElementById("tipo").value;
        const tombo = document.getElementById("tombo").value;
        const edificacao = document.getElementById("edificacao_value").value;

        const json = {
            "ambiente": ambiente,
            "tipo": parseInt(tipo),
            "tombo": tombo,
            "codigo_edificacao": edificacao,
        };

        const responsePonto = await fetch("/api/v1/pontos/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        });

        if (!responsePonto.ok) {
            const errorResponse = await responsePonto.json();
            throw new Error(`Erro ao criar o ponto: ${responsePonto.statusText}. Detalhes: ${JSON.stringify(errorResponse)}`);
        }

        const responseJson = await responsePonto.json();

        const formData = new FormData();

        const imagem = document.getElementById("foto");
        if (imagem.files.length > 0) {
            formData.append("imagem", imagem.files[0]);
        }

        const responseImagem = await fetch("/api/v1/pontos/" + responseJson.id + "/imagem", {
            method: 'POST',
            body: formData,
        });

        if (!responseImagem.ok) {
            const errorResponseImagem = await responseImagem.json();
            throw new Error(`Erro ao enviar a imagem: ${responseImagem.statusText}. Detalhes: ${JSON.stringify(errorResponseImagem)}`);
        }

        window.location.href = "/pontos";

    } catch (error) {
        console.error('Erro durante a criação:', error);
    } finally {
        isCriando = false;
        bt_criar.disabled = false;
        bt_criar.innerHTML = "Criar";
    }
}

// Adicionando um event listener ao botão
document.getElementById("criar").addEventListener("click", criarPonto);

carregarOpcoesEdificacao();