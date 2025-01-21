# Gestão de Produtores Rurais

Aplicativo web para gestão de Produtores, Fazendas e Safras.

Através dessa APi é possível, adicionar, visualizer, buscar, editar e remover dados de produtores, rurais, fazendas e safras, através de consumo de seus endpoints.

# Autores:

* **Thiago Pires** - *Desenvolvedor Backend*

## Primeiros Passos:

Para execução do projeto em uma máquina de forma local é necessário ter a ferramene Docker Compose instalada, as isnsruções para instalação constam no [link](https://docs.docker.com/compose/install/).

Após a instalação do Docker Compose, clone o projeto siga as instruções contidas na seção Instalação.

## Requisitos do sistema:

* Python 3.10 [site](https://www.python.org/);
* FastApi [site](https://fastapi.tiangolo.com/);
* SqlAlchemy [site](https://www.sqlalchemy.org/);
* PostgreSQL [site](https://www.postgresql.org/),
* Docker [site](https://www.docker.com/)

## Instalção:

1. Acesse o diretório do projeto e renomeie o arquivo config,sample.py para config.py
```
cp config.sample.py config.py  
```
3. Acesse o diretório do projeto e execute o comando no terminal:
```
docker compose up --build   
```
1. Abra o link abaixo no navegador [http://0.0.0.0:8500/docs](http://0.0.0.0:8500/docs)


## Executando os testes:

1. Verifique se o container python_app esteja rodando
```
docker ps   
```
2. Acesse o bash do container
```
docker exec -it python_app bash
```
3. Execute o comando:
```
pytest
```

Para ver a cobertura dos testes siga os passos 1 e 2
4. Execute os comandos:
```
coverage run -m pytest
coverage report
```

P.S: Os os comandos abaixo também funcinam
```
docker exec -it python_app pytest
docker exec -it python_app coverage run -m pytest && coverage report
```

## Ferramentas utilizadas

* [Visual Studio Code](https://code.visualstudio.com/)
* [Google Chrome](https://www.google.pt/intl/pt-PT/chrome/?brand=CHBD&gclid=Cj0KCQjwn_LrBRD4ARIsAFEQFKt3kLTIsdU6a-sk3FKsxrhplkKaYNHo6Pt3aRbaEAJ3TK4fZslZmtUaAvHVEALw_wcB&gclsrc=aw)
* [Docker](https://www.docker.com/)
