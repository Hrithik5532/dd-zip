from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25)
    
    def __str__(self) :
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=25)
    
    def __str__(self) :
        return self.name



veg_or_Nonveg_choice= (
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
   
    )
class Product(models.Model):
    name = models.CharField(max_length=25)
    img = models.ImageField(upload_to='Products/',verbose_name='Image')
    category = models.ManyToManyField(Category,null=True,blank=True)
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,null=True,blank=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=9999,null=True,blank=True)
    
    veg_or_Nonveg = models.CharField(max_length=20, choices=veg_or_Nonveg_choice,null=True,blank=True)

    meta_tags = models.TextField(null=True,blank=True)
    meta_description = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Menu Item"  # Singular name for the model
        verbose_name_plural = "Menu Items"