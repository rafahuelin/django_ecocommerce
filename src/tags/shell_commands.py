"""

from products.models import Product
qs = Product.objects.all()
qs
<ProductQuerySet [<Product: T-shirt>, <Product: Hat>, <Product: Supercomputer>, <Product: T-shirt>, <Product: Lorem Ipsum>]>
tshirt = qs.first()
tshirt
<Product: T-shirt>
tshirt.title()
Traceback (most recent call last):
  File "<input>", line 1, in <module>
TypeError: 'str' object is not callable
tshirt.title
'T-shirt'
tshirt.tag_set
<django.db.models.fields.related_descriptors.create_forward_many_to_many_manager.<locals>.ManyRelatedManager object at 0x00000274C34E0B00>
tshirt.tag_set.all()
<QuerySet [<Tag: T shirt>, <Tag: TShirt>, <Tag: T-shirt>, <Tag: Red>, <Tag: Black>]>

"""