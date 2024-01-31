from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Fornecedor
from src.schemas import FornecedorSchema, FornecedorList

router = APIRouter(prefix='/fornecedores', tags=['fornecedores'])

Session = Annotated[Session, Depends(get_session)]

@router.post('/', status_code=201)
def add_fornecedor(fornecedor: FornecedorSchema, session: Session):
    db_fornecedor = session.scalar(
        select(Fornecedor).where(Fornecedor.nome == fornecedor.nome)
    )
    if db_fornecedor:
        raise HTTPException(status_code=400, detail='Fornecedor já registrado!')

    db_fornecedor = Fornecedor(
        nome=fornecedor.nome, empresa=fornecedor.empresa, email=fornecedor.email, telefone=fornecedor.telefone
    )
    session.add(db_fornecedor)
    session.commit()
    session.refresh(db_fornecedor)

    return {'status': 'created', 'detail': 'Fornecedor registrado com sucesso!'}

@router.get('/', response_model=FornecedorList, status_code=200)
def get_fornecedores(session: Session):
    fornecedores = session.scalars(select(Fornecedor)).all()

    return {'fornecedores': fornecedores}

@router.get('/{fornecedor_id}')
def get_fornecedor(fornecedor_id: int, session: Session):
    fornecedor = session.scalar(select(Fornecedor).where(Fornecedor.id == fornecedor_id))

    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado!")

    return fornecedor

@router.put('/{fornecedor_id}')
def update_fornecedor(fornecedor_id: int, session: Session, fornecedor: FornecedorSchema):
    new_fornecedor = session.scalar(select(Fornecedor).where(Fornecedor.id == fornecedor_id))

    if not new_fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado!")

    new_fornecedor.nome = fornecedor.nome
    new_fornecedor.empresa = fornecedor.empresa
    new_fornecedor.email = fornecedor.email
    new_fornecedor.telefone = fornecedor.telefone

    session.add(new_fornecedor)
    session.commit()
    session.refresh(new_fornecedor)

    return {'status': 'updated', 'detail': 'Fornecedor atualizado com sucesso!'}

@router.delete('/{fornecedor_id}')
def delete_fornecedor(fornecedor_id: int, session: Session):
    fornecedor = session.scalar(select(Fornecedor).where(Fornecedor.id == fornecedor_id))

    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado!")

    session.delete(fornecedor)
    session.commit()

    return {'status': 'deleted', 'detail': 'Fornecedor deletado com sucesso!'}
