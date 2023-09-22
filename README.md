## O que é o projeto:
Está é uma aplicação de controle financeiro, aonde você pode realizar resgate, investimento na sua conta poupança, realizar consulta de saldo e extrato.

### Como rodar a aplicação(Para testar)?
- Dentro da root do projeto rode o comando 🐳:
    - ```docker-compose up --build```
- E ta pronto o sorvetinho 🍧

#### Caso queira rodar para mexer no codigo, como faço?
Por uma decisão de tempo, optei por não colocar um hotreload no compose, porém caso queira testar aplicação fuçar o código e etc siga os passos:

- Crie um ambiente virtual com ```python -m nome_ambiente venv```
- ative ele:
    - Windows: nome_ambiente\Scripts\Activate
    - Linux/mac: ```source nome_ambiente/bin/activate```
- Instale as dependencias: ```pip install -r requirements.txt```
- Rode as migrations: ```python manage.py migrate```
- Rode o projeto: ```python manage.py runserver```

### Para acessar o swagger:
- ```http://localhost:8000/swagger/```
- ```http://localhost:8000/redoc/```


##### Como rodar os testes?
- Rode o comando: ```python manage.py test```