from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class User(AbstractUser):
    avatar = models.ImageField(upload_to = 'catalog/image/%Y/%m')

class Genre(models.Model):
    name = models.CharField(max_length = 20, help_text='Enter a book name')

    def __str__(self):
        return self.name

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author is a string rather than an object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    price = models.IntegerField()
    
    summary = RichTextField()

    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    image = models.ImageField(upload_to='catalog/image/%Y/%m', height_field=None, width_field=None, max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class CartItem(models.Model):

    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)

    quantity = models.IntegerField(default=1)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book}{ "    --số lượng:  " }{self.quantity}'


class Cart(models.Model):

    items = models.ManyToManyField(CartItem, blank = True)

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


STAR_CHOICES = [

    (1, 'Mot Sao'),
    (2, 'Hai Sao'),
    (3, 'Ba Sao'),
    (4, 'Bon Sao'),
    (5, 'Nam Sao'),

] 

class Comment(models.Model):
    
    star = models.PositiveSmallIntegerField(choices=STAR_CHOICES)

    content = models.TextField(max_length=1000)

    assessor = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)

    book = models.ForeignKey('Book', on_delete=models.CASCADE, null=True)