import __init__
from views.view import SubscriptionService
from models.database import engine
from datetime import datetime
from decimal import Decimal
from models.model import Subscription

class UI:
    def __init__(self):
        self.subscriptions_service = SubscriptionService(engine)
    
    def start(self):
        while True:
            print('''
            [1] -> Adicionar assinatura
            [2] -> Remover assinatura
            [3] -> Valor total
            [4] -> Gastos últimos 12 meses
            [5] -> Pagar
            [6] -> Sair
            ''')
            
            choice = int(input('Escolha uma opção: '))
            
            if choice == 1:
                self.add_subscription()
            elif choice == 2:
                self.delete_subscription()
            elif choice == 3:
                self.total_value()
            elif choice == 4:
                self.subscriptions_service.gen_chart()
            elif choice == 5:
                self.pay()
            else:
                break
            
    def add_subscription(self):
        empresa = input('Nome da empresa: ')
        site = input('Site: ')
        data_assinatura = datetime.strptime(input('Data da assinatura: '), '%d/%m/%Y')
        valor = Decimal(input('Valor: '))
        subscription = Subscription(empresa=empresa, site=site, data_assinatura=data_assinatura, valor=valor)
        self.subscriptions_service.create(subscription)
        
    def delete_subscription(self):
        subscriptions = self.subscriptions_service.list_all()
        print('Escolha a qual assinatura deseja excluir: ')
        
        for i in subscriptions:
            print(f'[{i.id}] -> {i.empresa}')
            
        choice = int(input('Escolha a assinatura: '))
        self.subscriptions_service.delete(choice)
        print('Assinatura excluída com sucesso!')
        
    def total_value(self):
        print(f'Seu valor total mensal em assinaturas é: {self.subscriptions_service.total_value()}')
        
UI().start()