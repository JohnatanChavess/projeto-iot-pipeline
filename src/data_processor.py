import pandas as pd
from sqlalchemy import create_engine
import os

DB_USER = 'postgres'
DB_PASSWORD = '33131580' # <-- TROQUE AQUI PELA SUA SENHA
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'IOT-temp.csv')


def process_and_insert_data():
    """
    Lê os dados de temperatura do arquivo CSV e os insere em uma tabela no PostgreSQL.
    """
    try:
        engine = create_engine(DATABASE_URL)
        print("Conexão com o PostgreSQL estabelecida com sucesso.")

        print(f"Lendo dados de: {DATA_PATH}")
        df = pd.read_csv(DATA_PATH)
        print("Arquivo CSV lido com sucesso. Primeiras linhas do DataFrame:")
        print(df.head())


        df.rename(columns={
            'id': 'device_id',
            'room_id/id': 'room_id',
            'noted_date': 'timestamp'
        }, inplace=True)

        print("Inserindo dados na tabela 'temperature_readings'...")
        df.to_sql('temperature_readings', engine, if_exists='replace', index=False)
        print("Dados inseridos com sucesso no PostgreSQL!")

    except FileNotFoundError:
        print(f"Erro: O arquivo CSV não foi encontrado em '{DATA_PATH}'. Verifique o caminho.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    process_and_insert_data()