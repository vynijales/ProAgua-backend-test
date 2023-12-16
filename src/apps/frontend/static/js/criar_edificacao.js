let isCriandoEdificacao = false;

async function criarEdificacao() {
    if (isCriandoEdificacao) {
        console.log("Já existe uma requisição em andamento");
        return;
    }

    isCriandoEdificacao = true;
    const bt_criar = document.getElementById("criar");
    bt_criar.disabled = true;
    bt_criar.innerHTML = "Criando...";

    try {
        const codigo = document.getElementById("codigo").value;
        const nome = document.getElementById("nome").value;
        const campus = document.getElementById("campus").value;
        const cronograma = document.getElementById("cronograma").value;

        const json = {
            "codigo": codigo,
            "nome": nome,
            "campus": campus,
            "cronograma": parseInt(cronograma),
        };

        const response = await fetch("/api/v1/edificacoes/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(`Erro ao criar a edificação: ${response.statusText}. Detalhes: ${JSON.stringify(errorResponse)}`);
        }

        let formData = new FormData();
        const imagem = document.getElementById("foto");

        if (imagem.files.length > 0) {
            formData.append("imagem", imagem.files[0]);
            const responseImagem = await fetch("/api/v1/edificacoes/" + codigo + "/imagem", {
                method: 'POST',
                body: formData,
            })

            if (!responseImagem.ok) {
                throw new Error('Erro ao enviar a imagem');
            }
        }

        window.location.href = "/edificacoes";

    } catch (error) {
        console.error('Erro durante a criação:', error);
    } finally {
        isCriandoEdificacao = false;
        bt_criar.disabled = false;
        bt_criar.innerHTML = "Criar";
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

document.getElementById("criar").addEventListener("click", criarEdificacao);