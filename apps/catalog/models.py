from django.db import models

# Create your models here.
class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        db_column="parent_id",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "categories"
        ordering = ["sort_order", "name"]
    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    categories = models.ManyToManyField(
        Category,
        through="ProductCategory",
        related_name="products",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    image_url = models.CharField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    original_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    discount_label = models.CharField(max_length=50, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
    def __str__(self) -> str:
        return self.name

class ProductCategory(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_categories",
        db_column="product_id",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="product_categories",
        db_column="category_id",
    )
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_categories"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "category"],
                name="uq_product_categories_product_category",
            )
        ]
        indexes = [
            models.Index(fields=["category"], name="idx_pc_category"),
            models.Index(fields=["product"], name="idx_pc_product"),
            models.Index(
                fields=["product", "is_primary"],
                name="idx_pc_product_primary",
            ),
        ]
    def __str__(self) -> str:
        return f"product={self.product_id}, category={self.category_id}"