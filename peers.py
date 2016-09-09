from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import scopes

from tlsbase import TlsRelation


class TlsPeer(TlsRelation):
    '''This class uses the unit scope to communicate with individual peers.'''
    scope = scopes.UNIT

    @hook('{peers:tls}-relation-joined')
    def joined(self):
        '''When peers join set the create certificate signing request state.'''
        # Get the conversation scoped to the unit name.
        conv = self.conversation()
        # Set the start state here for the layers to handle the logic.
        conv.set_state('create certificate signing request')

    @hook('{peers:tls}-relation-changed')
    def changed(self):
        '''Only the leader should change the state to sign the request. '''
        # Get the conversation scoped to the unit name.
        conv = self.conversation()
        # Normaly we do not get the conversation this way, but for the peer
        # relation we want to get the value for this unit's conversation only.
        if hookenv.is_leader():
            if conv.get_remote('csr'):
                conv.set_state('sign certificate signing request')
        else:
            key = '{0}_signed_certificate'.format(hookenv.local_unit())
            if conv.get_remote(key):
                conv.set_state('signed certificate available')
