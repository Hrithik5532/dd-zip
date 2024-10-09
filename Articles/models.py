from django.db import models
from ckeditor.fields import RichTextField 
from taggit.managers import TaggableManager
# Create your models here.


class Articles(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to="Article-Thumbnail/")
    writer = models.CharField(max_length=20,null=True,blank=True)
    content = RichTextField(null=True, blank=True)
    created_at =models.DateField(auto_now_add=True)
    meta_tags = models.TextField()
    meta_description = models.TextField()
    tags = TaggableManager()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Articles"  # Singular name for the model
        verbose_name_plural = "Articles"
        
        
class Gallery(models.Model):
    img = models.ImageField(upload_to='Gallery/')
    
    class Meta:
        verbose_name = "Image Gallery"  # Singular name for the model
        verbose_name_plural = "Image Gallery"