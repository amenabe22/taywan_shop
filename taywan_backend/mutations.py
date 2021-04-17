import graphene
from django.db.models import F
from products.models import Product
from accounts.models import CustomUser
from django.contrib.auth import authenticate
from graphql_jwt.settings import jwt_settings
from orders.models import Cart, Order, PaymentType, BillingInfo, CartObject
from .types import(ProductType, TagsType, ColorsType, UsersType,
                   UsersAuthType, OrderType, BillingInfoType, PaymentTypeType)


class UpdateCart(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        cart = graphene.String()
        item = graphene.String()
        authed = graphene.Boolean()
        action = graphene.String()

    def mutate(self, info, cart, item, authed, action):
        actions = ["inc", "dec"]
        if not action in actions:
            raise Exception("action unknown")
        if authed:
            if not info.context.user.is_authenticated:
                raise Exception("user is not authenticated")
            cart = Cart.objects.filter(user=info.context.user)
            if not cart.exists():
                raise Exception("cart not found authed")
            try:
                if action == "dec":
                    cart[0].items.filter(id=item).update(amount=F('amount')-1)
                if action == "inc":
                    cart[0].items.filter(id=item).update(amount=F('amount')+1)
            except Exception as e:
                raise Exception(e)
        else:
            cart = Cart.objects.filter(anon_usr=cart)
            if not cart.exists():
                raise Exception("cart not found")
            try:
                if action == "dec":
                    cart[0].items.filter(id=item).update(amount=F('amount')-1)
                if action == "inc":
                    cart[0].items.filter(id=item).update(amount=F('amount')+1)
            except Exception as e:
                raise Exception(e)
        return RemoveCartItem(payload=True)


class RemoveCartItem(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        cart = graphene.String()
        item = graphene.String()
        authed = graphene.Boolean()

    def mutate(self, info, cart, item, authed):
        if authed:
            if not info.context.user.is_authenticated:
                raise Exception("user is not authenticated")
            cart = Cart.objects.filter(user=info.context.user)
            if not cart.exists():
                raise Exception("cart not found authed")
            try:
                cart[0].items.filter(id=item).delete()
            except Exception as e:
                raise Exception(e)
        else:
            cart = Cart.objects.filter(anon_usr=cart)
            if not cart.exists():
                raise Exception("cart not found")
            try:
                cart[0].items.filter(id=item).delete()
            except Exception as e:
                raise Exception(e)
        return RemoveCartItem(payload=True)


class AddToCartAnon(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        product = graphene.String()
        amount = graphene.Int()
        cart = graphene.String()

    def mutate(self, info, product, amount, cart):
        prod = Product.objects.filter(id=product)
        if not prod.exists():
            raise Exception("product not found")
        finCart = None
        userCart = Cart.objects.filter(anon_usr=cart)
        if userCart.exists():
            finCart = userCart[0]
        else:
            finCart = Cart.objects.create(anon_usr=cart)
        finCart.items.create(
            product=prod[0], amount=amount)
        return AddToCartUsr(payload=True)


class AddToCartUsr(graphene.Mutation):
    payload = graphene.Boolean()

    class Arguments:
        product = graphene.String()
        amount = graphene.Int()

    def mutate(self, info, product, amount):
        prod = Product.objects.filter(id=product)
        if not prod.exists():
            raise Exception("product not found")
        finCart = None
        userCart = Cart.objects.filter(user=info.context.user)
        if userCart.exists():
            finCart = userCart[0]
        else:
            finCart = Cart.objects.create(user=info.context.user)
        finCart.items.create(
            product=prod[0], amount=amount)
        return AddToCartUsr(payload=True)


class NewUserMutation(graphene.Mutation):
    payload = graphene.Field(UsersAuthType)

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        phone = graphene.String()
        email = graphene.String()
        birth_date = graphene.Date()
        password = graphene.String()
        cart_id = graphene.String()

    def mutate(self, info, first_name, last_name, phone, email, password, birth_date, cart_id):
        try:
            user = CustomUser.objects.create(
                email=email, first_name=first_name, last_name=last_name, phone=phone,
                birth_date=birth_date
            )
            user.username = str(user.user_id)
            user.set_password(password)
            user.save()
            # check cart status and creat a new one
            cart = Cart.objects.filter(anon_usr=cart_id)
            if cart.exists():
                print('HEYYYYYY')
                cart.update(user=user, anonnymous=False)
            else:
                Cart.objects.create(
                    user=user, anonnymous=False, anon_usr=cart_id)
            usr = authenticate(request=info.context.session,
                               username=email, password=password)
            payload = jwt_settings.JWT_PAYLOAD_HANDLER(usr, info.context)
            token = jwt_settings.JWT_ENCODE_HANDLER(payload, info.context)

        except Exception as e:
            raise Exception(e)
        return NewUserMutation(payload={"udata": user, "token": token})


class AddOrder(graphene.Mutation):
    payload = graphene.Field(OrderType)

    class Arguments:
        full_name = graphene.String()
        phone = graphene.String()
        address_line = graphene.String()
        city = graphene.String()
        region = graphene.String()
        payment = graphene.String()

    def mutate(self, info, full_name, phone, address_line, city, region, payment):
        user = info.context.user
        userCart = Cart.objects.filter(user=user)
        billingInfo = BillingInfo.objects.create(
            address_line=address_line, city=city, full_name=full_name, phone=phone, region=region
        )
        # check payment option availablity
        payment_opt = PaymentType.objects.filter(type_id=payment)
        if not payment_opt.exists():
            raise Exception("payment type unknown")
        order = Order.objects.create(
            paid_already=False, ordered_by=user,
            billing_info=billingInfo,
            payment_type=payment_opt[0])
        # order.billing_info
        if not userCart[0].items.exists():
            raise Exception("cart is empty")

        for cart in userCart[0].items.all():
            order.products.create(
                product=cart.product
            )
        # clear the cart after checkout
        userCart[0].items.all().delete()
        return AddOrder(payload=order)
