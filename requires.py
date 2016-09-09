from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import scopes

from tlsbase import TlsRelation


class TlsRequires(TlsRelation):
    '''The class that requires a TLS relationship to another unit.'''
    scope = scopes.UNIT


    @hook('{peers:tls}-relation-changed')
    def changed(self):
        '''Only the leader should change the state to sign the request. '''
        # Get the conversation scoped to the unit name.
        conv = self.conversation()
        key = '{0}_signed_certificate'.format(hookenv.local_unit())
        if conv.get_remote(key):
            conv.set_state('signed certificate available')
