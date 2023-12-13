let isAtualizando = false;
let isExcluindo = false;

function carregarEdificacao() {
    let target = window.location.pathname.split("/edificacoes/")[1];
    target = target.replace(/\/$/, "");

    fetch("/api/v1/edificacoes/" + target, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => {
            if (!response.ok) {
                window.location.href = "/edificacoes/";
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            document.getElementById("codigo").value = data.codigo;
            document.getElementById("nome").value = data.nome;
            document.getElementById("campus").value = data.campus;
            document.getElementById("cronograma").value = data.cronograma;

            var formAction = "/api/v1/edificacoes/" + target;
            document.getElementById("edificacaoForm").action = formAction;
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function atualizarEdificacao() {
    if (isAtualizando) {
        console.log("A atualização já está em andamento...");
        return;
    }

    isAtualizando = true;

    const bt_atualizar = document.getElementById("atualizar");
    bt_atualizar.disabled = true;
    bt_atualizar.innerHTML = "Atualizando...";

    let target = window.location.pathname.split("/edificacoes/")[1];
    target = target.replace(/\/$/, "");

    var codigo = document.getElementById("codigo").value;
    var nome = document.getElementById("nome").value;
    var campus = document.getElementById("campus").value;
    var cronograma = document.getElementById("cronograma").value;

    var json = {
        "codigo": codigo,
        "nome": nome,
        "campus": campus,
        "cronograma": parseInt(cronograma)
    };

    try {
        fetch("/api/v1/edificacoes/" + target, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json)
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                window.location.href = "/edificacoes";
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    } catch (error) {
        console.error('Erro durante a atualização:', error);
    } finally {
        isAtualizando = false;
        bt_atualizar.disabled = false;
        bt_atualizar.innerHTML = "Atualizar";
    }
}

function excluirEdificacao() {
    if (isExcluindo) {
        console.log("A exclusão já está em andamento...");
        return;
    }

    isExcluindo = true;

    const bt_excluir = document.getElementById("excluir");
    bt_excluir.disabled = true;
    bt_excluir.innerHTML = "Excluindo...";

    let target = window.location.pathname.split("/edificacoes/")[1];
    target = target.replace(/\/$/, "");

    var json = {};

    try {
    fetch("/api/v1/edificacoes/" + target, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(json)
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            window.location.href = "/edificacoes";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    } catch (error) {
        console.error('Erro durante a exclusão:', error);
    } finally {
        isExcluindo = false;
        bt_excluir.disabled = false;
        bt_excluir.innerHTML = "Excluir";
    }
}

document.getElementById("atualizar").addEventListener("click", atualizarEdificacao);
document.getElementById("excluir").addEventListener("click", excluirEdificacao);

carregarEdificacao();