from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.urls import reverse
from transliterate import translit
from datetime import timedelta
from django.conf import settings

# Create your models here.
class Key(models.Model):
    key = models.CharField(max_length=20)

class Category(models.Model):
    name = models.CharField(max_length=124)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'category_slug': self.slug})


def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(translit(str(instance.name), reversed=True))
        instance.slug = slug


pre_save.connect(pre_save_category_slug, sender=Category)


class Publisher(models.Model):
    name = models.CharField(max_length=124)

    def __str__(self):
        return self.name


def image_folder(instance, filename):
    filename = instance.slug + '.' + filename.split('.')[-1]
    return '{0}/{1}'.format(instance.slug, filename)


class GameManager(models.Manager):

    def all(self, *args, **kwargs):
        return super(GameManager, self).get_queryset().filter(available=True)


class Game(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    title = models.CharField(max_length=124)
    description = models.TextField()
    slug = models.SlugField(null=True)
    image = models.ImageField(upload_to=image_folder)

    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    objects = GameManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'game_slug': self.slug})


class Cart(models.Model):
    product = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    item_cost = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    key = models.ForeignKey(Key, on_delete=models.CASCADE)

    def __str__(self):
        return 'Корзина {} {} {}'.format(self.product.title, self.key.key, self.item_cost)


class Order(models.Model):
    carts = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    cvv = models.CharField(max_length=3)
    card = models.CharField(max_length=16)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return 'Замовлення {} {}'.format(self.user.username, str(self.date + timedelta(hours=3)).split('.')[0])


