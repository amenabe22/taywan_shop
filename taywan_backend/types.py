import graphene
from accounts.models import CustomUser
from graphene_django import DjangoObjectType
from orders.models import Cart, CartObject, Order, BillingInfo, PaymentType
from products.models import Color, Tag, Product, Category, ParentCategory


class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class BillingInfoType(DjangoObjectType):
    class Meta:
        model = BillingInfo


class PaymentTypeType(DjangoObjectType):
    class Meta:
        model = PaymentType


class UsersType(DjangoObjectType):
    class Meta:
        model = CustomUser


class UsersAuthType(graphene.ObjectType):
    udata = graphene.Field(UsersType)
    token = graphene.String()


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class TagsType(DjangoObjectType):
    class Meta:
        model = Tag


class ColorsType(DjangoObjectType):
    class Meta:
        model = Color


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class CartType(DjangoObjectType):
    class Meta:
        model = Cart


class CartTypeType(DjangoObjectType):
    class Meta:
        model = CartObject


class ParentCategoryType(DjangoObjectType):
    class Meta:
        model = ParentCategory
