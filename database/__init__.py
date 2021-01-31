from . import notifications, common, subscription_secret_store
import functools

subscription_secrets = subscription_secret_store.SubscriptionSecretStore()

# named like this because on the user's side, the syntax looks like:
# @database.is_used
# def func_that_uses_db(): ...
def is_used(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        common.init_db()
        try:
            return func(*args, **kwargs)
        finally:
            common.teardown_db()
    return inner
