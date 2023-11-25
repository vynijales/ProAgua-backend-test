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
    var ambiente = document.getElementById("ambiente").value;
    var tipo = document.getElementById("tipo").value;
    var tombo = document.getElementById("tombo").value;
    var edificacao = document.getElementById("edificacao_value").value;
    
    var imagem = document.getElementById("foto");

    var json = {
        "ambiente": ambiente,
        "tipo": parseInt(tipo),
        "tombo": tombo,
        "codigo_edificacao": edificacao,
    };

    try {
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

        responseJson = await responsePonto.json();
        
        let formData = new FormData();

        if (imagem.files.length > 0) {
            formData.append("imagem", imagem.files[0]);
        }

        const responseImagem = await fetch("/api/v1/pontos/" + responseJson.id + "/imagem", {
            method: 'POST',
            body: formData,
        });

        if (!responseImagem.ok) {
            throw new Error('Erro ao enviar a imagem');
        }
        
        window.location.href = "/ponto";

    } catch (error) {
        console.error('Erro durante a criação:', error);
    }

}

carregarOpcoesEdificacao();