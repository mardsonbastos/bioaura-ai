# BioAura AI

Aplicação Streamlit responsiva para cadastro, histórico, organização de avaliações com IA e geração de PDF.

## Executar localmente

1. Instale Python 3.11+.
2. Crie ambiente virtual:
   `python -m venv .venv`
3. Ative o ambiente.
4. Instale:
   `pip install -r requirements.txt`
5. Configure as variáveis do `.env.example` no ambiente/segredos do servidor.
6. Execute:
   `streamlit run app.py`

## Celular

Depois de publicar em um servidor compatível com Streamlit, abra o endereço pelo navegador do Android. A interface é responsiva e pode ser adicionada à tela inicial pelo navegador.

## Produção

Antes de usar com dados reais, configure HTTPS, autenticação robusta, backups, controle de acesso, auditoria, política de privacidade e medidas de segurança compatíveis com a LGPD. Não coloque a chave da OpenAI dentro do código.

A IA deste projeto é para apoio à organização/revisão das informações fornecidas e não deve substituir avaliação profissional nem gerar prescrição automática.
