from typing import List

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import FileResponse
from ninja import Router, Query
from ninja.pagination import paginate

from io import BytesIO
from io import StringIO

from .schemas.coleta import *
from .schemas.usuario import UsuarioOut
from .. import models

import pandas as pd

router = Router(tags=["Coletas"])


@router.get("/", response=List[ColetaOut])
@paginate
def list_coleta(request, filter: FilterColeta = Query(...)):
    qs = models.Coleta.objects.all()
    return filter.filter(qs).order_by("data")


@router.get("/csv", response=List[ColetaOut])
def get_coletas_csv(request, filter: FilterColeta = Query(...)):
    coletas = filter.filter(models.Coleta.objects.all().order_by("data"))
    csv_headers = [
        "id", "temperatura", "cloro_residual_livre", "turbidez", "coliformes_totais",
        "escherichia", "cor", "data", "responsaveis", "ordem", "sequencia_id", "ponto_id"
    ]
    csv_file = StringIO()
    csv_file.write(",".join(csv_headers) + "\n")
    for coleta in coletas:
        csv_file.write(
            f"{coleta.id},{coleta.temperatura},{coleta.cloro_residual_livre},{coleta.turbidez},{coleta.coliformes_totais},{coleta.escherichia},{coleta.cor},{coleta.data},{'/'.join([str(r.username) for r in coleta.responsavel.all()])},{coleta.ordem},{coleta.sequencia.id},{coleta.ponto.id}\n"
        )
    csv_file.seek(0)
    return FileResponse(BytesIO(csv_file.getvalue().encode()), as_attachment=True, filename="coletas.csv")


@router.get("/excel", response=List[ColetaOut])
def get_coletas_excel(request, filter: FilterColeta = Query(...)):
    coletas = filter.filter(models.Coleta.objects.all().order_by("data"))
    df = pd.DataFrame(list(coletas.values()))
    # Remove timezone information from the "data" column
    df["data"] = df["data"].dt.tz_localize(None)
    def rename(x): return "Presença" if x else "Ausência"
    df["escherichia"] = df["escherichia"].apply(rename)
    df["coliformes_totais"] = df["coliformes_totais"].apply(rename)

    df = df.rename(columns={
        "id": "ID",
        "temperatura": "Temperatura",
        "cloro_residual_livre": "Cloro Residual Livre",
        "turbidez": "Turbidez",
        "coliformes_totais": "Coliformes Totais",
        "escherichia": "Escherichia coli",
        "cor": "Cor Aparente",
        "data": "Data",
        "ordem": "Ordem",
        "sequencia_id": "ID Sequência",
        "ponto_id": "ID Ponto",
        "status": "Status",
        "status_message": "Mensagem de Status"
    })

    # Criar colunas de Edificacao

    df.insert(1, "Código da Edificação", "DEFAULT")
    df.insert(2, "Nome da Edificação", "DEFAULT")
    df.insert(3, "Campus", "DEFAULT")

    # Criar colunas de Ponto
    df.insert(4, "Tipo", "DEFAULT")
    df.insert(5, "Ambiente", "DEFAULT")
    df.insert(6, "Tombo", "DEFAULT")

    # Inserindo os valores correspondentes nas colunas criadas
    for index, row in df.iterrows():
        ponto = models.PontoColeta.objects.filter(id=row["ID Ponto"]).first()
        if ponto:
            edificacao = models.Edificacao.objects.filter(
                id=ponto.edificacao_id).first()
            if edificacao:
                df.at[index, "Código da Edificação"] = str(
                    edificacao.codigo)  # Explicitly convert to string
                df.at[index, "Nome da Edificação"] = str(
                    edificacao.nome)  # Explicitly convert to string
                df.at[index, "Campus"] = edificacao.campus
            df.at[index, "Tipo"] = ponto.get_tipo_display()
            df.at[index, "Ambiente"] = ponto.ambiente
            df.at[index, "Tombo"] = ponto.tombo

    # Renomeando campus
    def rename_campus(x): return "Leste" if str(
        x) == "LE" else "Oeste" if str(x) == "OE" else "Null"
    df["Campus"] = df["Campus"].apply(rename_campus)

    # Removendo as colunas ID Sequência e ID Ponto
    df = df.drop(columns=["ID Sequência", "ID Ponto",
                 "Status", "Mensagem de Status"])

    excel_file = BytesIO()
    writer = pd.ExcelWriter(excel_file, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Coletas", index=False)

    # Ajustando a largura das colunas
    for column in df:
        if column != "ID":
            column_min_width = 10
        else:
            column_min_width = 5
        column_length = max(df[column].astype(str).map(
            len).max(), len(column), column_min_width)
        col_idx = df.columns.get_loc(column)
        writer.sheets['Coletas'].set_column(col_idx, col_idx, column_length)

    writer.close()
    excel_file.seek(0)
    return FileResponse(excel_file, as_attachment=True, filename="coletas.xlsx")


@router.get("/{id_coleta}", response=ColetaOut)
def get_coleta(request, id_coleta: int):
    qs = get_object_or_404(models.Coleta, id=id_coleta)
    return qs


@router.post("/")
def create_coleta(request, payload: ColetaIn):
    data_dict = payload.dict()
    responsavel_ids = data_dict.get("responsavel", [])

    # Removendo a lista de responsáveis do dicionário para criar a instância da Coleta
    del data_dict["responsavel"]

    obj_seq = get_object_or_404(
        models.SequenciaColetas, id=data_dict.get("sequencia_id"))

    data_dict["status"] = None
    data_dict["status_message"] = None

    # Criando a instância da Coleta sem os responsáveis
    obj_coleta = models.Coleta.objects.create(**data_dict, sequencia=obj_seq)

    # Use o método set para adicionar os responsáveis após a criação
    for responsavel_id in responsavel_ids:
        user = User.objects.filter(id=responsavel_id).first()
        if user:
            obj_coleta.responsavel.add(user)

    return {"success": True}


@router.put("/{id_coleta}")
def update_coleta(request, id_coleta: int, payload: ColetaIn):
    obj_coleta = get_object_or_404(models.Coleta, id=id_coleta)
    data_dict = payload.dict()
    responsavel_ids = data_dict.get("responsavel", [])

    # Removendo a lista de responsáveis do dicionário
    del data_dict["responsavel"]

    # Iterando sobre os campos no payload e atualizar os valores correspondentes na instância
    for attr, value in data_dict.items():
        setattr(obj_coleta, attr, value)

    # Atualizando os responsáveis
    obj_coleta.responsavel.clear()
    for responsavel_id in responsavel_ids:
        user = User.objects.filter(id=responsavel_id).first()
        if user:
            obj_coleta.responsavel.add(user)

    obj_coleta.save()

    return {"success": True}


@router.delete("/{id_coleta}")
def delete_coleta(request, id_coleta: int):
    obj_coleta = get_object_or_404(models.Coleta, id=id_coleta)
    obj_coleta.delete()
    return {"success": True}


@router.get("/{id_coleta}/responsaveis", response=List[UsuarioOut])
def get_responsaveis_coleta(request, id_coleta: int):
    coleta = get_object_or_404(models.Coleta, id=id_coleta)
    return coleta.responsavel
