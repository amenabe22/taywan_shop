import graphql
import graphene
import graphql_jwt
from accounts.models import CustomUser
from orders.models import Cart, PaymentType
from django_graphene_permissions import permissions_checker
from products.models import Product, Category, ParentCategory
from django_graphene_permissions.permissions import IsAuthenticated
from .mutations import NewUserMutation, AddToCartUsr, AddToCartAnon, RemoveCartItem, UpdateCart, AddOrder
from .types import ProductType, TagsType, ColorsType, UsersType, CategoryType, CartType, ParentCategoryType, PaymentTypeType


class Query(graphene.ObjectType):
    user_data = graphene.Field(UsersType)
    all_prods = graphene.List(ProductType)
    prod_detail = graphene.Field(ProductType, slug=graphene.String())
    related_cat_prods = graphene.List(
        ProductType, cat=graphene.String(), prod=graphene.String())
    user_cart = graphene.List(
        CartType, anon=graphene.Boolean(), cart=graphene.String())
    cats = graphene.List(ParentCategoryType)
    cat_prods = graphene.List(ProductType, cat=graphene.String())
    payment_options = graphene.List(PaymentTypeType)

    def resolve_payment_options(self, info):
        return PaymentType.objects.filter(available=True)

    def resolve_related_cat_prods(self, info, cat, prod):
        prod = Product.objects.filter(id=prod)
        if not prod.exists():
            raise Exception("product not found")
        cat = Category.objects.filter(id=cat)
        if not cat.exists():
            return Product.objects.none()
        prods = Product.objects.filter(category=cat[0]).exclude(id=prod[0].id)
        return prods

    def resolve_cat_prods(self, info, cat):
        cat = Category.objects.filter(id=cat)
        if not cat.exists():
            return Product.objects.none()
        prods = Product.objects.filter(category=cat[0])
        return prods

    def resolve_cats(self, info):
        return ParentCategory.objects.all()

    def resolve_user_cart(self, info, anon, cart):
        if anon:
            cart = Cart.objects.filter(anon_usr=cart)
        else:
            if not info.context.user.is_authenticated:
                raise Exception("User is not authenticated")
            cart = Cart.objects.filter(user=info.context.user)
        return cart

    @permissions_checker([IsAuthenticated])
    def resolve_user_data(self, info):
        user = CustomUser.objects.filter(user_id=info.context.user.user_id)
        if not user.exists():
            raise Exception("user not found")
        return user[0]

    def resolve_prod_detail(self, info, slug):
        prod = Product.objects.filter(slug=slug)
        if not prod.exists():
            raise Exception("product not found")
        return prod[0]

    def resolve_all_prods(self, info):
        prods = Product.objects.all()
        return prods


class Mutations(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    new_user = NewUserMutation.Field(description="New user creation API")
    add_cart_anon = AddToCartAnon.Field(
        description="Load To Cart for Anon people")
    add_cart_usr = AddToCartUsr.Field(description="Add to cart for users")
    remove_cart_item = RemoveCartItem.Field()
    update_cart = UpdateCart.Field()
    add_order = AddOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
