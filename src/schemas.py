from pydantic import BaseModel, ConfigDict


class FornecedorSchema(BaseModel):
    id: int | None = None
    nome: str
    empresa: str
    email: str
    telefone: str

class FornecedorList(BaseModel):
    fornecedores: list[FornecedorSchema]

class ProdutoSchema(BaseModel):
    id: int | None = None
    nome: str
    quantidade_estoque: int
    quantidade_vendida: int
    preco_unico: float
    receita: float

class ProdutoList(BaseModel):
    produtos: list[ProdutoSchema]
