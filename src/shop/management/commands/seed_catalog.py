from django.core.management.base import BaseCommand

from shop.models import Product


PRODUCTS = [
    {
        "slug": "moldura-classica",
        "name": "Moldura clássica",
        "category": Product.Category.MOLDURAS,
        "summary": "Um acabamento atemporal para paredes e tetos.",
        "description": "Moldura decorativa em gesso para compor ambientes com elegância. O perfil, as medidas e a instalação são definidos conforme o espaço.",
        "price_from": "38.00",
        "image_url": "/static/shop/img/artdecor-interior.webp",
        "image_alt": "Molduras de gesso organizadas no ateliê Art Decor",
        "featured": True,
    },
    {
        "slug": "coluna-canelada",
        "name": "Coluna canelada",
        "category": Product.Category.MOLDURAS,
        "summary": "Volume e textura para um detalhe arquitetônico marcante.",
        "description": "Elemento canelado para valorizar entradas, paredes e composições clássicas ou contemporâneas. Produzida conforme altura, diâmetro e acabamento definidos no orçamento.",
        "price_from": None,
        "image_url": "/static/shop/img/artdecor-profile-work.jpg",
        "image_alt": "Coluna canelada de gesso em produção no ateliê",
        "featured": True,
    },
    {
        "slug": "boiserie-personalizada",
        "name": "Boiserie personalizada",
        "category": Product.Category.BOISERIE,
        "summary": "Molduras que desenham ritmo e personalidade na parede.",
        "description": "Composição de molduras decorativas desenhada para as proporções da parede. Consulte a equipe para definir medidas, quantidade de quadros e instalação.",
        "price_from": "85.00",
        "image_url": "/static/shop/img/artdecor-interior.webp",
        "image_alt": "Perfis e molduras de gesso fabricados pela Art Decor",
        "featured": True,
    },
    {
        "slug": "sanca-de-gesso",
        "name": "Sanca de gesso",
        "category": Product.Category.SANCAS,
        "summary": "Um arremate leve para transformar a luz do ambiente.",
        "description": "Sancas e cortineiros em gesso, com opções de desenho e iluminação indireta. O preço de referência não inclui iluminação nem instalação.",
        "price_from": "68.00",
        "image_url": "/static/shop/img/artdecor-profile-work.jpg",
        "image_alt": "Detalhe de acabamento em gesso canelado",
        "featured": True,
    },
    {
        "slug": "painel-de-tv",
        "name": "Painel de TV",
        "category": Product.Category.PAINEIS,
        "summary": "Uma composição sob medida para a parede principal.",
        "description": "Painel decorativo com molduras e detalhes em gesso, planejado para o tamanho da parede e a posição dos equipamentos. Valor final após medidas.",
        "price_from": None,
        "image_url": "/static/shop/img/artdecor-interior.webp",
        "image_alt": "Perfis de gesso disponíveis para composições decorativas",
        "featured": False,
    },
    {
        "slug": "banco-para-jardim",
        "name": "Banco de cimento",
        "category": Product.Category.JARDIM,
        "summary": "Desenho contemporâneo para jardins e áreas externas.",
        "description": "Banco em cimento para valorizar jardins, varandas e áreas de convivência. Consulte disponibilidade, dimensões, acabamento e entrega.",
        "price_from": None,
        "image_url": "/static/shop/img/artdecor-garden.webp",
        "image_alt": "Banco de cimento contemporâneo em jardim iluminado, imagem do perfil Art Decor",
        "featured": False,
    },
    {
        "slug": "reparo-em-gesso",
        "name": "Reparo em gesso",
        "category": Product.Category.REPAROS,
        "summary": "Correção cuidadosa para devolver unidade ao acabamento.",
        "description": "Reparos em molduras, sancas e outros acabamentos de gesso. Envie fotos e medidas aproximadas para uma avaliação inicial.",
        "price_from": None,
        "image_url": "/static/shop/img/artdecor-profile-work.jpg",
        "image_alt": "Trabalho de acabamento em gesso no ateliê Art Decor",
        "featured": False,
    },
    {
        "slug": "peca-em-fibra-de-vidro",
        "name": "Peça em fibra de vidro",
        "category": Product.Category.FIBRA,
        "summary": "Leveza e liberdade de formas para projetos especiais.",
        "description": "Peças decorativas em fibra de vidro desenvolvidas conforme a necessidade do projeto. Formato, acabamento e prazo são definidos em orçamento.",
        "price_from": None,
        "image_url": "/static/shop/img/artdecor-detail.webp",
        "image_alt": "Modelos de colunas decorativas exibidos no perfil Art Decor",
        "featured": False,
    },
]


class Command(BaseCommand):
    help = "Carrega um catálogo demonstrativo da Art Decor."

    def handle(self, *args, **options):
        for data in PRODUCTS:
            Product.objects.update_or_create(slug=data["slug"], defaults=data)
        self.stdout.write(self.style.SUCCESS(f"{len(PRODUCTS)} peças carregadas no catálogo."))