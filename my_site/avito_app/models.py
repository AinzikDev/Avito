from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from unicodedata import category

USER_STATUS = (
     ('simple', 'simple'),
     ('bronze', 'bronze'),
     ('silver', 'silver'),
     ('gold', 'gold'),
)


class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MaxValueValidator(70), MinValueValidator(18)],
                                           null=True, blank=True)

    phone_number = PhoneNumberField(default='+996')
    avatar = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=USER_STATUS, default='simple')
    date_registered = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
      category_name = models.CharField(max_length=100, unique=True)
      category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)

      def __str__(self):
          return self.category_name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'category_sub')
    subcategory_name = models.CharField(max_length=100, unique=True)
    subcategory_image= models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return f'{self.category.category_name}-{self.subcategory_name}'


class Product(models.Model):
        category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_product')
        subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
        product_name = models.CharField(max_length=100)
        description = models.TextField(null=True, blank=True)
        price = models.DecimalField(max_digits=10, decimal_places=2)
        product_image = models.ImageField(upload_to='product_images/')
        product_type = models.BooleanField(default=False)
        created_date = models.DateField(auto_now_add=True)
        article = models.PositiveBigIntegerField(unique=True)

        def __str__(self):
            return f'{self.subcategory.subcategory_name}-{self.product_name}'

        def get_avg_rating(self):
            ratings = self.product_review.all()
            if ratings.exists():
                return round(sum([i.stars for i in ratings]) / ratings.count(), 1)
            return 0

        def get_count_rating(self):
            return self.product_review.count()


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_img')
    product_image = models.ImageField(upload_to='product_images/')


class Reviews(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_review')
    review_image = models.ImageField(upload_to='review_images/', null=True, blank=True)
    stars = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} — comment'

class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def get_total_price(self):
        return sum([i.get_total_price() for i in self.item.all()])

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.product.price

class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class FavoriteItem(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE, related_name='favorite_item')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)