from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import scopes

from tlsbase import TlsRelation


class TlsProvides(TlsRelation):
    '''The class that provides a TLS interface other units.'''
    scope = scopes.UNIT

    @hook('{provides:tls}-relation-joined')
    def joined(self):
        '''When a unit joins create a certificate signing request state.'''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        # Set the request state for the layer to handle the logic.
        conversation.set_state('create certificate signing request')
        conversation.set_state('send certificate authority')

    @hook('{provides:tls}-relation-changed')
    def changed(self):
        '''Only the leader should change the state to sign the request.'''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        if hookenv.is_leader():
            if conversation.get_remote('csr'):
                conversation.set_state('sign certificate signing request')
