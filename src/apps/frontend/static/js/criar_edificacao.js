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

        window.location.href = "/edificacao";

    } catch (error) {
        console.error('Erro durante a criação:', error);
    } finally {
        isCriandoEdificacao = false;
        bt_criar.disabled = false;
        bt_criar.innerHTML = "Criar";
    }
}

document.getElementById("criar").addEventListener("click", criarEdificacao);