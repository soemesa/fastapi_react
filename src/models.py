
from sqlalchemy import String, ForeignKey, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase):
    pass


class Produto(BaseModel):
    __tablename__ = "produto"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(30), nullable=False)
    quantidade_estoque: Mapped[int] = mapped_column(default=0)
    quantidade_vendida: Mapped[int] = mapped_column(default=0)
    preco_unico: Mapped[float] = mapped_column(Float(precision=8, decimal_return_scale=2), default=0.00)
    receita: Mapped[float] = mapped_column(Float(precision=8, decimal_return_scale=2), default=0.00)

    fornecedor = relationship('Fornecedor', back_populates='produto')
    fornecido_por: Mapped[int] = mapped_column(ForeignKey('fornecedor.id'))


class Fornecedor(BaseModel):
    __tablename__ = "fornecedor"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(20))
    empresa: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(100))
    telefone: Mapped[str] = mapped_column(String(15))

    produto = relationship('Produto', back_populates='fornecedor')

