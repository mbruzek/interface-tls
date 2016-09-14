import json
import os
import sys

from charms.reactive import hook
from charms.reactive import scopes
from charms.reactive import RelationBase


class TlsProvides(RelationBase):
    '''The class that provides a TLS interface other units.'''
    scope = scopes.UNIT

    @hook('{provides:tls}-relation-joined')
    def joined(self):
        '''When a unit joins set a available state.'''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        conversation.set_state('{relation_name}.available')

    @hook('{provides:tls}-relation-changed')
    def changed(self):
        '''x'''
        conversation = self.conversation()
        cn = conversation.get_remote('common_name')
        sans = conversation.get_remote('sans')
        name = conversation.get_remote('certificate_name')
        if cn and sans and name:
            conversation.set_state('{relation_name}.server.cert.requested')

    @hook('{provides:tls}-relation-{broken,departed}')
    def broken_or_departed(self):
        '''Remove the states that were set.'''
        conversation = self.conversation()
        conversation.remove_state('{relation_name}.available')

    def set_ca(self, certificate_authority):
        '''Set the CA on all the conversations in the relation data.'''
        # Iterate over all conversations of this type.
        for conversation in self.conversations():
            conversation.set_remote(data={'ca': certificate_authority})

    def set_client_cert(self, cert, key):
        '''Set the client cert and key on the relation data.'''
        # Iterate over all conversations of this type.
        for conversation in self.conversations():
            client = {}
            client['client.cert'] = cert
            client['client.key'] = key
            conversation.set_remote(data=client)

    def set_server_cert(self, scope, cert, key):
        '''Set the server cert and key on the relation data.'''
        # Get the coversation 
        conversation = self.conversation(scope)
        server = {}
        server['server.cert'] = cert
        server['server.key'] = key
        conversation.set_remote(data=server)
        conversation.remove_state('{relation_name}.server.cert.requested')

    def get_server_requests(self):
        '''Return a map of all server request objects indexed by the name or
        scope.'''
        request_map = {}
        for conversation in self.conversations():
            scope = conversation.scope
            request = {}
            request['common_name'] = conversation.get_remote('common_name')
            request['sans'] = json.loads(conversation.get_remote('sans'))
            request['certificate_name'] = conversation.get_remote('certificate_name')  # noqa
            request_map[scope] = request
        return request_map
