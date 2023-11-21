function openNav() {
    document.getElementById('sidebar').style.width = '15em';
}

function closeNav() {
    document.getElementById('sidebar').style.width = '0';
}

function carregarEdificacao() {
    let target = window.location.pathname.split("/edificacao/")[1];
    target = target.replace(/\/$/, "");

    fetch("/api/v1/edificacoes/" + target, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => {
            if (!response.ok) {
                window.location.href = "{% url 'visualizar_edificacoes' %}";
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
    console.log("Atualizando edificação...");
    let target = window.location.pathname.split("/edificacao/")[1];
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
            window.location.href = "/edificacao";
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

carregarEdificacao();