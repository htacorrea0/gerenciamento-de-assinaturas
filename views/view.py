import __init__
from models.database import engine
from models.model import Subscription
from datetime import date
from sqlmodel import Session, select #uma session é de fato a conexão com o bd, agora eu posso escrever nele pois estou conectada, logada

class SubscriptionService:
    def __init__(self, engine): #classe construtora, self se referencia a própria classe
        self.engine = engine
    
    def create(self, subscription: Subscription): #função que salva uma subscription no bd. tem como parametro subscription e é do tipo Subscription, ou seja, tem todos os dados da tabela (nome, site, id etc)
        with Session(self.engine) as session: #criei uma session. with abre e fecha arquivos, nesse caso o do bd
            session.add(subscription) #adiciona em uma camada intermediaria entre o python e o bd
            session.commit() #adiciona no bd
            return subscription
    
    def list_all(self): #vai listar todas as assinaturas
        with Session(self.engine) as session:
            statement = select(Subscription) #select de bd mesmo
            result = session.exec(statement).all()
        return result
            

ss = SubscriptionService(engine)
#subscription = Subscription(empresa='Pythonando', site='pythonando.com.br', data_assinatura=date.today(), valor=35.9)
#ss.create(subscription)
print(ss.list_all())