from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class Produto(BaseModel):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(30), nullable=False)
    quantidade_estoque: Mapped[int] = mapped_column(default=0)
    quantidade_vendida: Mapped[int] = mapped_column(default=0)
    preco_unico: Mapped[float] = mapped_column(max_digits=8, decimal_places=2, default=0.00)
    receita: Mapped[float] = mapped_column(max_digits=20, decimal_places=2, default=0.00)

    fornecedor: Mapped[int] = mapped_column(ForeignKey('fornecedor.id'))


class Fornecedor(BaseModel):
    __tablename__ = "fornecedor"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(20))
    empresa: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    telefone: Mapped[str] = mapped_column(String(15))

