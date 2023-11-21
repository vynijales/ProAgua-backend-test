function criarEdificacao() {
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

    fetch("/api/v1/edificacoes/", {
        method: 'POST',
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