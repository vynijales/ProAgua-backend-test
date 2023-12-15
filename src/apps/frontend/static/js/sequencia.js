const BASE_URL = "";
const container = document.getElementById("container");

async function getSequenciaColetas(id) {
    let response = await fetch(`${BASE_URL}/api/v1/sequencias/${id}`);
    if (!response.ok) {
        throw new Error(`Erro ao acessar a API: ${response.statusText}`);
    }
    return await response.json();
}

function groupColetaByPonto(coletas) {
    let groups = [];
    let current_group = {
        ponto: coletas[0].ponto_url,
        coletas: []
    };
    
    coletas.forEach((coleta) => {
        if (current_group.ponto != coleta.ponto_url) {
            groups.push(current_group);
            current_group = {
                ponto: coleta.ponto_url,
                coletas: []
            };
        }
        current_group.coletas.push(coleta);
    });

    groups.push(current_group);

    return groups;
}

async function createTableColetas(data) {
    const columns = [
        '-',
        'Ordem',
        'Temperatura',
        'Cloro residual livre',
        'Turbidez',
        'Coliformes totais',
        'Escherichia coli',
        'Cor',
        'Data',
        'Responsável',
        'Status',
        'Editar'
    ];
    const table = document.createElement("table");
    const header_row = document.createElement("tr");
    const body_rows = [];

    // Create table header
    columns.forEach(value => {
        let th = document.createElement('th');
        th.innerText = value.toString();
        header_row.appendChild(th);
    });
    
    // Create table rows
    data.forEach((coleta) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${coleta.id}</td>
            <td>${coleta.ordem}</td>
            <td>${coleta.temperatura}</td>
            <td>${coleta.cloro_residual_livre}</td>
            <td>${coleta.turbidez}</td>
            <td>${coleta.coliformes_totais
            ? 'Presença'
            : 'Ausência'}</td>
            <td>${coleta.escherichia
            ? 'Presença'
            : 'Ausência'}</td>
            <td>${coleta.cor}</td>
            <td>${coleta.data}</td>
            <td>${coleta.responsaveis_url}</td>
            <td style="text-align: center;">${coleta.status.status
            ? '<i class="bi bi-check2"></i>'
            : '<i class="bi bi-x"></i>'}
            ${coleta.status.message}
            </td>
            <td>
                <a href="#edit/${coleta.id}">Editar</a>
            </td>
        `;
        body_rows.push(row);
    });
    table.append(header_row, ...body_rows);
    return table;
}

getSequenciaColetas(1).then(sequencia => {
    let grupos = groupColetaByPonto(sequencia.coletas);

    grupos.forEach(grupo => {
        let title = document.createElement('h3');
        if (grupo.ponto) {
            title.innerText = String(grupo.ponto).toString();
        }
        
        createTableColetas(grupo.coletas).then(table => {
            container?.append(title);
            container?.append(table);
        });

    });
});
