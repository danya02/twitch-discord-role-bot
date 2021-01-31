from .common import SubscriptionSecret

class SubscriptionSecretStore:
    def __getitem__(self, name):
        try:
            ss = SubscriptionSecret.get(twitch_id=name)
            if isinstance(ss.value, bytes): return ss.value
            else: return bytes(ss.value, 'ascii')
        except SubscriptionSecret.DoesNotExist: raise KeyError('secret not found')
    def __setitem__(self, name, value):
        value = bytes(value, 'ascii')
        try:
            ss = SubscriptionSecret.get(twitch_id=name)
            ss.value = value
            ss.save()
        except SubscriptionSecret.DoesNotExist:
            SubscriptionSecret.create(twitch_id=name, value=value)
    def __delitem__(self, name):
        deleted = SubscriptionSecret.delete().where(SubscriptionSecret.twitch_id == name).execute()
        if deleted == 0: raise KeyError('no such secrets found')

