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
            document.getElementsByTagName("form").action = formAction;

            console.log(data.imagem);
            const imageUrl = data.imagem;

            const imgElement = document.getElementById("imagePreview");
            imgElement.src = imageUrl;

            console.log(imageUrl)

        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

async function atualizarPonto() {

    if (isAtualizando) {
        console.log("A atualização já está em andamento...");
        return;
    }

    isAtualizando = true;

    const bt_atualizar = document.getElementById("atualizar");
    bt_atualizar.disabled = true;
    bt_atualizar.innerHTML = "Atualizando...";

    let target = window.location.pathname.split("/ponto/")[1];
    target = target.replace(/\/$/, "");

    var id = document.getElementById("id").value;
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
        const responsePonto = await fetch("/api/v1/pontos/" + target, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        });

        if (!responsePonto.ok) {
            const errorResponse = await responsePonto.json();
            throw new Error(`Erro ao atualizar o ponto: ${responsePonto.statusText}. Detalhes: ${JSON.stringify(errorResponse)}`);
        }
        
        let formData = new FormData();

        if (imagem.files.length > 0) {
            formData.append("imagem", imagem.files[0]);
            const responseImagem = await fetch("/api/v1/pontos/" + target + "/imagem", {
                method: 'POST',
                body: formData,
            })
            
            if (!responseImagem.ok) {
                throw new Error('Erro ao enviar a imagem');
            }
        }
        ;

       

        window.location.href = "/ponto";

    } catch (error) {
        console.error('Erro durante a atualização:', error);
    } finally {
        isAtualizando = false;
    }
}

async function excluirPonto() {

    if (isDeletando) {
        console.log("A exclusão já está em andamento...");
        return;
    }

    isDeletando = true;

    const bt_excluir = document.getElementById("excluir");
    bt_excluir.disabled = true;
    bt_excluir.innerHTML = "Excluindo...";

    let target = window.location.pathname.split("/ponto/")[1];
    target = target.replace(/\/$/, "");

    var json = {};

    try {
        const responsePonto = await fetch("/api/v1/pontos/" + target, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(json),
        });

        console.log('Ponto atualizado com sucesso:', await responsePonto.json());
        
        window.location.href = "/pontos";
    } catch (error) {
        console.error('Erro durante a exclusão:', error);
    } finally {
        isAtualizando = false;
        bt_atualizar.disabled = false;
        bt_atualizar.innerHTML = "Atualizar";
    }
}

async function atualizarEdificacao() {
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
    var imagem = document.getElementById("foto");

    try {
        const response = await fetch("/api/v1/edificacoes/" + target, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                codigo,
                nome,
                campus,
                cronograma
            }),
        });

        if (!response.ok) {
            const errorResponse = await response.json();
            throw new Error(`Erro ao atualizar a edificação: ${response.statusText}. Detalhes: ${JSON.stringify(errorResponse)}`);
        }

        let formData = new FormData();

        if (imagem.files.length > 0) {
            formData.append("imagem", imagem.files[0]);
            const responseImagem = await fetch("/api/v1/edificacoes/" + target + "/imagem", {
                method: 'POST',
                body: formData,
            })
        
            if (!responseImagem.ok) {
                throw new Error('Erro ao enviar a imagem');
            }
        }

        window.location.href = "/edificacoes";

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

document.getElementById("atualizar").addEventListener("click", atualizarEdificacao);
document.getElementById("excluir").addEventListener("click", excluirEdificacao);

carregarEdificacao();

