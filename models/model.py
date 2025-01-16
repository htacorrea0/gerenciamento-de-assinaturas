from sqlmodel import Field, Relationship, SQLModel # type: ignore
from typing import Optional #deixa opcional o site na tabela
from datetime import date
from decimal import Decimal

class Subscription(SQLModel, table=True): #herdo as coisas de sqlmodel e informo que a classe comporta como uma tabela
    id: int = Field(primary_key=True)
    empresa: str
    site: Optional[str] = None #se eu passar, o tipo tem que ser str, se não, não tem tipo (none)
    data_assinatura: date
    valor: Decimal
    
class Payments(SQLModel, table=True):
    id: int = Field(primary_key=True)
    subscription_id: int = Field(foreign_key='subscription.id')
    subscription: Subscription = Relationship()
    date: date    