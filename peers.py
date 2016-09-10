import os
import sys

from charmhelpers.core import hookenv
from charms.reactive import hook
from charms.reactive import scopes
sys.path.append(os.path.dirname(__file__))
from tlsbase import TlsRelation


class TlsPeer(TlsRelation):
    '''This class uses the unit scope to communicate with individual peers.'''
    scope = scopes.UNIT

    @hook('{peers:tls}-relation-joined')
    def joined(self):
        '''When peers join set the create certificate signing request state.'''
        # Get the conversation scoped to the unit.
        conversation = self.conversation()
        # Set the start state here for the layers to handle the logic.
        conversation.set_state('{relation_name}.create.csr')
        conversation.set_state('{relation_name}.send.ca')

    @hook('{peers:tls}-relation-changed')
    def changed(self):
        '''Only the leader should change the state to sign the request. '''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        # Normaly we do not get the conversation this way, but for the peer
        # relation we want to get the value for this unit's conversation only.
        if hookenv.is_leader():
            if conversation.get_remote('csr'):
                conversation.set_state('{relation_name}.sign.csr')
        else:
            key = '{0}_signed_certificate'.format(hookenv.local_unit())
            if conversation.get_remote(key):
                conversation.set_state('{relation_name}.signed')
