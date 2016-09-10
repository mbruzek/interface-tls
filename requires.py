import os
import sys

from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import scopes
sys.path.append(os.path.dirname(__file__))
from tlsbase import TlsRelation


class TlsRequires(TlsRelation):
    '''The class that requires a TLS relationship to another unit.'''
    scope = scopes.UNIT

    @hook('{peers:tls}-relation-joined')
    def joined(self):
        '''When peers join set the create certificate signing request state.'''
        # Get the conversation scoped to the unit.
        conversation = self.conversation()
        # Set the start state here for the layers to handle the logic.
        conversation.set_state('{relation_name}.create.csr')

    @hook('{peers:tls}-relation-changed')
    def changed(self):
        '''Only the leader should change the state to sign the request. '''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        key = 'ca'
        if conversation.get_remote(key):
            conversation.set_state('{relation_name}.store.ca')
        key = '{0}_signed_certificate'.format(hookenv.local_unit())
        if conv.get_remote(key):
            conv.set_state('{relation_name}.signed')
