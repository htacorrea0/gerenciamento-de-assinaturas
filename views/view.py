import __init__
import matplotlib.pyplot as plt
from models.database import engine
from models.model import Subscription, Payments
from datetime import date, datetime
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
    
    def delete(self, id):
        with Session(self.engine) as session:
            statement = select(Subscription).where(Subscription.id == id)
            result = session.exec(statement).one()#.one pq so vai retornar um valor por ser primary key
            session.delete(result)
            session.commit()
    
    def _has_pay(self, results):
        for result in results:
            if result.date.month == date.today().month:
                return True
        return False
          
    def pay(self, subscription: Subscription):
        with Session(self.engine) as session:
            statement = select(Payments).join(Subscription).where(Subscription.empresa==subscription.empresa) #conferindo se eu já paguei a conta. esse subscription.empresa se refere a empresa da linha logo abaixo de inserção (subscription = Subscription(empresa='Pythonando'.... por ex.)
            results = session.exec(statement).all()
            if self._has_pay(results): #se retornar que foi pago
                question = input('Essa conta já foi paga esse mês, deseja pagar novamente? Y ou N: ')
                
                if not question.upper() == 'Y': #se digitar diferente de y
                    return
                
            pay = Payments(subscription_id=subscription.id, date=date.today()) #o primeiro subscription.id se refere ao da tabela e o segundo ao que recebemos como parametro em pay, e estamos acessando o id dele
            session.add(pay)
            session.commit()
    
    def total_value(self):
        with Session(self.engine) as session:
            statement = select(Subscription)
            results = session.exec(statement).all()
            
        total = 0
        for result in results:
            total += result.valor
        
        return float(total)
    
    def _get_last_12_months_native(self):
        today = datetime.now()
        year = today.year
        month = today.month
        
        last_12_month = []
        for _ in range(12):
            last_12_month.append((month, year))
            month -= 1
            if month == 0:
                month = 12
                year -= 1
                
        return last_12_month[::-1]
    
    def _get_values_for_months(self, last_12_month):
        with Session(self.engine) as session:
            statement = select(Payments)
            results = session.exec(statement).all()
            
            value_for_months = []
            
            for i in last_12_month:
                value = 0
                for result in results:
                    if result.date.month == i[0] and result.date.year == i[1]:
                        value += float(result.subscription.valor)
                value_for_months.append(value)
            return value_for_months
                
    def gen_chart(self):
        last_12_months = self._get_last_12_months_native()
        values_for_months = self._get_values_for_months(last_12_months)
        last_12_months_labels = list(map(lambda x: f"{x[1]}-{x[0]:02d}", last_12_months))
        
        plt.plot(last_12_months_labels, values_for_months)
        plt.xlabel('Month-Year')
        plt.ylabel('Total Value')
        plt.title('Total Value for Last 12 Months')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
                
ss = SubscriptionService(engine)
print(ss.gen_chart())
