from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Fornecedor, Produto
from src.schemas import ProdutoSchema, ProdutoList

router = APIRouter(prefix='/produtos', tags=['produtos'])

Session = Annotated[Session, Depends(get_session)]


@router.post('/{fornecedor_id}', status_code=201, response_model=None)
def create_produto(
        fornecedor_id: int,
        produto: ProdutoSchema,
        session: Session
):
    fornecedor = session.scalar(select(Fornecedor).where(Fornecedor.id == fornecedor_id))

    if not fornecedor:
        raise HTTPException(status_code=404, detail='Fornecedor não encontrado!')

    new_produto = session.scalar(
        select(Produto).where(Produto.nome == produto.nome)
    )
    if new_produto:
        raise HTTPException(status_code=400, detail='Produto já registrado!')

    new_produto = Produto(
        nome=produto.nome,
        quantidade_estoque=produto.quantidade_estoque,
        quantidade_vendida=produto.quantidade_vendida,
        preco_unico=produto.preco_unico,
        receita=produto.receita,
        fornecido_por=fornecedor.id
    )
    session.add(new_produto)
    session.commit()
    session.refresh(new_produto)

    return {'status': 'created', 'detail': 'Produto registrado com sucesso!'}

@router.get('/', response_model=ProdutoList)
def get_produtos(session: Session):
    produtos = session.scalars(select(Produto)).all()
    return {'produtos': produtos}

@router.get('/{produto_id}')
def get_produto(produto_id: int, session: Session):
    db_produto = session.scalar(select(Produto).where(Produto.id == produto_id))

    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado!")

    return db_produto

@router.put('/{produto_id}')
def update_produto(produto_id: int, produto: ProdutoSchema, session: Session):
    new_produto = session.scalar(select(Produto).where(Produto.id == produto_id))

    if not new_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado!")

    new_produto.nome = produto.nome
    new_produto.quantidade_estoque = produto.quantidade_estoque
    new_produto.quantidade_vendida = produto.quantidade_vendida
    new_produto.preco_unico = produto.preco_unico
    new_produto.receita = produto.receita

    session.add(new_produto)
    session.commit()
    session.refresh(new_produto)

    return {'status': 'updated', 'detail': 'Produto atualizado com sucesso!'}

@router.delete('/{produto_id}')
def delete_produto(produto_id: int, session: Session):
    produto = session.scalar(select(Produto).where(Produto.id == produto_id))

    if not produto:
        raise HTTPException(status_code=404, detail='Produto não encontrado')

    session.delete(produto)
    session.commit()

    return {'status': 'deleted', 'detail': 'Produto deletado com sucesso!'}
