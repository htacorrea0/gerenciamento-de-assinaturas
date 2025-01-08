from sqlmodel import Field, SQLModel, create_engine
from .model import *

sqlite_file_name = 'database.bd'
sqlite_url = f'sqlite:///{sqlite_file_name}' #url de conexão com o bd

#engine é a conexão do python com o bd. Sabe qual o bd ceto, onde está, se é SQL, sabe seu usuário e senha etc
engine = create_engine(sqlite_url, echo=True)#echo vai escrever no terminal as coisas do engine

if __name__ == '__main__': #__name__ é uma variavel do python que, quando a gente roda um arquivo, ele fala de onde foi rodado. Ou seja, se não estivermos executando o arquivo por ele mesmo na main (ou seja, importando), o if vai ser pulado.
    SQLModel.metadata.create_all(engine) #SQl vai verificar todas as classes que herdam de SQl e table=true e vai criar as tabelas (dentro da onde a engine foi criada)