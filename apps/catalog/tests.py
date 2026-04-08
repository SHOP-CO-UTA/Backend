# from rest_framework import status
# from rest_framework.test import APITestCase

# from .models import Category, Product, ProductCategory, ProductVariant


# class ProductRetrieveApiTests(APITestCase):
#     def setUp(self):
#         self.category = Category.objects.create(
#             name="T-shirts",
#             slug="t-shirts",
#             is_active=True,
#             sort_order=1,
#         )
#         self.product = Product.objects.create(
#             name="One Life Graphic T-shirt",
#             slug="one-life-graphic-tshirt",
#             description="A soft cotton graphic tee.",
#             image_url="/images/products/one-life.png",
#             price="260.00",
#             original_price="300.00",
#             discount_label="-30%",
#             rating="4.50",
#             stock=50,
#         )
#         ProductCategory.objects.create(
#             product=self.product,
#             category=self.category,
#             is_primary=True,
#         )
#         ProductVariant.objects.create(
#             product=self.product,
#             color="#8B7355",
#             size="Large",
#             stock=12,
#             sku="OLG-L-OLIVE",
#         )

#     def test_get_product_detail_by_id_returns_200(self):
#         response = self.client.get(f"/catalog/products/{self.product.id}/")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["id"], self.product.id)
#         self.assertEqual(response.data["name"], self.product.name)
#         self.assertIn("variants", response.data)
#         self.assertEqual(len(response.data["variants"]), 1)
#         self.assertIn("primary_category", response.data)
#         self.assertEqual(response.data["primary_category"]["slug"], self.category.slug)

#     def test_get_product_detail_by_id_not_found_returns_404(self):
#         response = self.client.get("/catalog/products/999999/")
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
