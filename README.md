# Art Decor

Loja de apresentação e pedidos da Art Decor / Art cimento, construída com Django, templates e uma organização DDD por domínio, aplicação, infraestrutura e apresentação.

## Requisitos

- Python 3.11 ou superior
- PowerShell no Windows

## Preparar e executar

No PowerShell, a partir desta pasta:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:PYTHONPATH = "src"
python manage.py migrate
python manage.py seed_catalog
python manage.py seed_carousel
python manage.py runserver
```

Abra `http://127.0.0.1:8000/`. O painel administrativo fica em `/admin/`; crie um usuário com `python manage.py createsuperuser` para gerenciar catálogo, pedidos e slides dos carrosséis.

## Estrutura

- `src/shop/domain`: entidades, valores de domínio e contratos dos repositórios.
- `src/shop/application`: casos de uso, incluindo validação e envio de pedidos.
- `src/shop/infrastructure`: adaptadores Django/ORM e persistência.
- `src/shop/presentation`: views, rotas e contexto dos templates.
- `templates/shop`: páginas Django renderizadas no servidor.
- `static/shop`: identidade visual, JavaScript e imagens locais do perfil público da marca.

## Catálogo e pedidos

`python manage.py seed_catalog` carrega oito itens demonstrativos e pode ser executado novamente sem duplicá-los. Preços exibidos são referências iniciais fictícias para apresentar o fluxo; confirme valores e condições com a Art Decor antes de publicar a loja. Serviços sob medida são enviados para orçamento.

O checkout registra nome, contato, itens, observações e forma de pagamento escolhida. Pix, cartão e dinheiro são combinados diretamente com o atendimento. Não há gateway conectado, cobrança automática ou coleta de dados de cartão. A chave Pix oficial ainda precisa ser informada pela empresa antes de qualquer solicitação de pagamento.

O catálogo é paginado em blocos de seis itens, preservando filtros e busca. A ação de adicionar ao pedido aceita resposta JSON para atualizar o contador sem recarregar; formulários HTML continuam disponíveis como fallback. O indicador de carregamento só aparece quando uma navegação ou requisição ultrapassa 400 ms, evitando cintilação nas respostas rápidas. Consultas de catálogo retornam apenas os campos usados pela interface e usam índice composto para os filtros mais comuns.

Os carrosséis da home e da página Sobre são alimentados por slides ativos do banco, ordenados por página e posição. Edite texto, imagem, botão, ordem e visibilidade em `/admin/` sem alterar os templates. `python manage.py seed_carousel` prepara os slides de demonstração usando fotos locais do perfil público do Instagram; o logo local em `static/shop/img/instagram-logo.jpg` é a imagem de perfil pública de `@gesso.artdecor`.

Contato de atendimento consultado no Instagram público: WhatsApp `(62) 9 8223-0022`. As fotografias locais foram obtidas de publicações públicas de `@gesso.artdecor` para compor esta prévia; confirme autorização e substitua ou atualize os arquivos antes da publicação comercial.

## Verificações

```powershell
$env:PYTHONPATH = "src"
python manage.py check
python manage.py test shop
```

Antes de publicar, defina `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` e `DJANGO_ALLOWED_HOSTS` para o ambiente de produção. Configure HTTPS, backup do banco de dados, política de privacidade e detalhes de entrega/garantia conforme as regras comerciais da Art Decor.