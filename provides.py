import os
import sys

from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import scopes
sys.path.append(os.path.dirname(__file__))
from tlsbase import TlsRelation


class TlsProvides(TlsRelation):
    '''The class that provides a TLS interface other units.'''
    scope = scopes.UNIT

    @hook('{provides:tls}-relation-joined')
    def joined(self):
        '''When a unit joins create a certificate signing request state.'''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        conversation.set_state('{relation_name}.send.ca')

    @hook('{provides:tls}-relation-changed')
    def changed(self):
        '''Only the leader should change the state to sign the request.'''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        if hookenv.is_leader():
            if conversation.get_remote('csr'):
                conversation.set_state('{relation_name}.sign.csr')
