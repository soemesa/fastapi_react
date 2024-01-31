from pydantic import BaseModel


class FornecedorSchema(BaseModel):
    id: int | None = None
    nome: str
    empresa: str
    email: str
    telefone: str

class FornecedorList(BaseModel):
    fornecedores: list[FornecedorSchema]