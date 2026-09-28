from django.core.management.base import BaseCommand

from shop.models import CarouselSlide


SLIDES = [
    {
        "page": CarouselSlide.Page.HOME,
        "order": 1,
        "eyebrow": "ART DECOR · GOIÁS",
        "title": "O detalhe que faz a casa",
        "accent": "ser sua.",
        "copy": "Gesso, cimento e fibra de vidro trabalhados com cuidado, da primeira ideia ao acabamento.",
        "image_url": "/static/shop/img/artdecor-profile-work.jpg",
        "image_alt": "Peça canelada de gesso feita pela Art Decor",
        "button_label": "Explorar catálogo",
        "button_url": "/catalogo/",
    },
    {
        "page": CarouselSlide.Page.HOME,
        "order": 2,
        "eyebrow": "ACABAMENTO EM GESSO",
        "title": "Formas que dão",
        "accent": "personalidade.",
        "copy": "Molduras e detalhes arquitetônicos para criar ambientes com presença e equilíbrio.",
        "image_url": "/static/shop/img/artdecor-interior.webp",
        "image_alt": "Perfis decorativos em gesso produzidos no ateliê",
        "button_label": "Conhecer o trabalho",
        "button_url": "/sobre/",
    },
    {
        "page": CarouselSlide.Page.HOME,
        "order": 3,
        "eyebrow": "CIMENTO · JARDIM",
        "title": "Desenho que encontra",
        "accent": "a natureza.",
        "copy": "Peças decorativas que conectam matéria, espaço e momentos de todos os dias.",
        "image_url": "/static/shop/img/artdecor-garden.webp",
        "image_alt": "Peça de cimento em um jardim, publicação da Art Decor",
        "button_label": "Ver peças",
        "button_url": "/catalogo/?categoria=jardim",
    },
    {
        "page": CarouselSlide.Page.ABOUT,
        "order": 1,
        "eyebrow": "NOSSA ESSÊNCIA",
        "title": "Matéria moldada com",
        "accent": "intenção.",
        "copy": "Cada peça nasce do encontro entre ofício, atenção aos detalhes e o jeito de morar de cada pessoa.",
        "image_url": "/static/shop/img/artdecor-interior.webp",
        "image_alt": "Acabamentos de gesso feitos no ateliê Art Decor",
        "button_label": "Ver nosso trabalho",
        "button_url": "/catalogo/",
    },
    {
        "page": CarouselSlide.Page.ABOUT,
        "order": 2,
        "eyebrow": "FEITO À MÃO",
        "title": "Cuidado em cada",
        "accent": "etapa.",
        "copy": "Escuta, medida e acabamento preciso: assim transformamos uma ideia em parte da sua casa.",
        "image_url": "/static/shop/img/artdecor-profile-work.jpg",
        "image_alt": "Trabalho artesanal em gesso da Art Decor",
        "button_label": "Conhecer o catálogo",
        "button_url": "/catalogo/",
    },
    {
        "page": CarouselSlide.Page.ABOUT,
        "order": 3,
        "eyebrow": "GESSO · CIMENTO · FIBRA",
        "title": "Beleza que respeita",
        "accent": "o espaço.",
        "copy": "Projetos sob medida e soluções para reformas, reparos e novos ambientes.",
        "image_url": "/static/shop/img/artdecor-detail.webp",
        "image_alt": "Detalhe de peça decorativa do perfil Art Decor",
        "button_label": "Fale com a equipe",
        "button_url": "https://wa.me/5562982230022",
    },
]


class Command(BaseCommand):
    help = "Carrega slides demonstrativos para os carrosséis da home e do sobre."

    def handle(self, *args, **options):
        for data in SLIDES:
            CarouselSlide.objects.get_or_create(
                page=data["page"],
                order=data["order"],
                defaults=data,
            )
        self.stdout.write(self.style.SUCCESS(f"{len(SLIDES)} slides preparados."))