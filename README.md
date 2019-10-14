# Tondellog

Geração de changelog personalizado.

Para instalar na sua máquina:
- Na pasta do app execute no cmd.

```
pip uninstall tondellog && python setup.py sdist && pip install dist/tondellog-0.0.1.tar.gz
```

Para configurar(opcional):

```
tondellog init
```

Para executar e gerar o changelog

```
tondellog output
```

Para gerar o changelog sem ter a configuração

```
tondellog output2 --host https://seuhost.com.br --group "seu grupo" --project "nome do seu projeto" --private_token "sua chave privada"
```