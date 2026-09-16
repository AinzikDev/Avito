import random

from django.core.management.base import BaseCommand
from django.db import transaction

from avito_app.models import Category, SubCategory, Product, Reviews, UserProfile


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными (категории, подкатегории, товары, отзывы) на EN и RU'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Удалить существующие Category/SubCategory/Product/Reviews перед заполнением',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['flush']:
            Reviews.objects.all().delete()
            Product.objects.all().delete()
            SubCategory.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Старые данные удалены.'))

        # ---------- Пользователи ----------
        user, created = UserProfile.objects.get_or_create(
            username='test_user',
            defaults={
                'first_name': 'Азамат',
                'last_name': 'Тестов',
                'email': 'test_user@example.com',
                'age': 25,
                'phone_number': '+996700123456',
                'status': 'bronze',
            },
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {user.username}'))

        # ---------- Категории (name_en / name_ru через modeltranslation) ----------
        categories_data = [
            {'en': 'Electronics', 'ru': 'Электроника'},
            {'en': 'Clothing', 'ru': 'Одежда'},
            {'en': 'Home & Garden', 'ru': 'Дом и сад'},
        ]

        categories = {}
        for cat in categories_data:
            obj, _ = Category.objects.get_or_create(
                category_name_en=cat['en'],
                defaults={'category_name_ru': cat['ru']},
            )
            # на случай если объект уже был, но без ru-перевода
            obj.category_name_ru = cat['ru']
            obj.category_name = cat['en']  # активный язык по умолчанию (MODELTRANSLATION_DEFAULT_LANGUAGE = 'en')
            obj.save()
            categories[cat['en']] = obj
            self.stdout.write(f'Категория: {cat["en"]} / {cat["ru"]}')

        # ---------- Подкатегории ----------
        subcategories_data = [
            {'category': 'Electronics', 'en': 'Smartphones', 'ru': 'Смартфоны'},
            {'category': 'Electronics', 'en': 'Laptops', 'ru': 'Ноутбуки'},
            {'category': 'Clothing', 'en': 'Men', 'ru': 'Мужская одежда'},
            {'category': 'Clothing', 'en': 'Women', 'ru': 'Женская одежда'},
            {'category': 'Home & Garden', 'en': 'Furniture', 'ru': 'Мебель'},
        ]

        subcategories = {}
        for sub in subcategories_data:
            obj, _ = SubCategory.objects.get_or_create(
                category=categories[sub['category']],
                subcategory_name_en=sub['en'],
                defaults={'subcategory_name_ru': sub['ru']},
            )
            obj.subcategory_name_ru = sub['ru']
            obj.subcategory_name = sub['en']
            obj.save()
            subcategories[sub['en']] = obj
            self.stdout.write(f'Подкатегория: {sub["en"]} / {sub["ru"]}')

        # ---------- Товары ----------
        products_data = [
            {
                'subcategory': 'Smartphones',
                'category': 'Electronics',
                'name_en': 'iPhone 15 Pro',
                'name_ru': 'iPhone 15 Про',
                'desc_en': 'Latest Apple flagship smartphone with A17 chip.',
                'desc_ru': 'Новейший флагманский смартфон Apple с чипом A17.',
                'price': 999.99,
            },
            {
                'subcategory': 'Laptops',
                'category': 'Electronics',
                'name_en': 'MacBook Air M2',
                'name_ru': 'MacBook Air M2',
                'desc_en': 'Lightweight and powerful laptop for everyday tasks.',
                'desc_ru': 'Лёгкий и мощный ноутбук для повседневных задач.',
                'price': 1199.00,
            },
            {
                'subcategory': 'Men',
                'category': 'Clothing',
                'name_en': 'Classic Denim Jacket',
                'name_ru': 'Классическая джинсовая куртка',
                'desc_en': 'Durable denim jacket, perfect for any season.',
                'desc_ru': 'Прочная джинсовая куртка, подходит на любой сезон.',
                'price': 59.90,
            },
            {
                'subcategory': 'Women',
                'category': 'Clothing',
                'name_en': 'Summer Floral Dress',
                'name_ru': 'Летнее платье с цветочным принтом',
                'desc_en': 'Light and comfortable dress for warm days.',
                'desc_ru': 'Лёгкое и удобное платье для тёплых дней.',
                'price': 39.50,
            },
            {
                'subcategory': 'Furniture',
                'category': 'Home & Garden',
                'name_en': 'Wooden Coffee Table',
                'name_ru': 'Деревянный журнальный столик',
                'desc_en': 'Solid wood coffee table with modern design.',
                'desc_ru': 'Журнальный столик из массива дерева в современном стиле.',
                'price': 149.99,
            },
        ]

        created_products = []
        for p in products_data:
            article = random.randint(10_000_000, 99_999_999)
            obj, _ = Product.objects.get_or_create(
                product_name_en=p['name_en'],
                defaults={
                    'category': categories[p['category']],
                    'subcategory': subcategories[p['subcategory']],
                    'product_name_ru': p['name_ru'],
                    'description_en': p['desc_en'],
                    'description_ru': p['desc_ru'],
                    'price': p['price'],
                    'article': article,
                },
            )
            obj.product_name = p['name_en']
            obj.description_ru = p['desc_ru']
            obj.description_en = p['desc_en']
            obj.save()
            created_products.append(obj)
            self.stdout.write(f'Товар: {p["name_en"]} / {p["name_ru"]} — {p["price"]}')

        # ---------- Отзывы ----------
        review_comments = [
            {'en': 'Great product, fast delivery!', 'ru': 'Отличный товар, быстрая доставка!'},
            {'en': 'Good value for money.', 'ru': 'Хорошее соотношение цены и качества.'},
            {'en': 'Not bad, but could be better.', 'ru': 'Неплохо, но могло быть и лучше.'},
        ]

        for product in created_products:
            comment = random.choice(review_comments)
            Reviews.objects.get_or_create(
                user=user,
                product=product,
                defaults={
                    'stars': random.randint(3, 5),
                    'comment': f"{comment['en']} / {comment['ru']}",
                },
            )

        self.stdout.write(self.style.SUCCESS('Готово! База успешно заполнена тестовыми данными.'))