from charmhelpers.core import hookenv
from charms.reactive import RelationBase
from charms.reactive import scopes


class TlsRelation(RelationBase):
    '''This class uses the unit scope to communicate with individual peers.'''
    scope = scopes.UNIT

    def get_ca(self):
        '''Return the certificate authority.'''
        # Get the conversation scoped to the unit.
        conversation = self.conversation()
        # Find the certificate authority by key, and return the value.
        return conversation.get_remote('ca')

    def get_signed_cert(self):
        '''Return the signed certificate from the relation data.'''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        # Normaly we do not get the conversation this way, but for the peer
        # relation we want to get the value for this unit's conversation only.
        key = '{0}_signed_certificate'.format(hookenv.local_unit())
        return conversation.get_remote(key)

    def get_csr_map(self):
        '''Return a map of name and csr for each unit requesting a signed cert.
        Encapsulate the communication for all the units in this peer relation.
        '''
        csr_map = {}
        # Get all conversations of this type.
        conversations = self.conversations()
        # For each converation get the name and csr put them in a map.
        for conversation in conversations:
            name = conversation.scope
            csr = conversation.get_remote('csr')
            csr_map[name] = csr
        return csr_map

    def set_ca(self, certificate_authority):
        '''Set the CA on all the conversations in the relation data.'''
        # Iterate over all conversations of this type.
        for conversation in self.conversations():
            conversation.set_remote(data={'ca': certificate_authority})

    def set_csr(self, csr):
        '''Set the certificate signing request (CSR) on the relation data.'''
        # Get the conversation scoped to the unit name.
        conversation = self.conversation()
        # Normaly we do not get the conversation this way, but for the peer
        # relation we want to set the value for this unit's conversation only.

        # Remove the old state.
        conversation.remove_state('create certificate signing request')
        # Set the value on the relation.
        conversation.set_remote(data={'csr': csr})
        # Normaly we do not get the conversation this way, but for the peer
        # relation we want to get the value for this unit's conversation only.
        key = '{0}_signed_certificate'.format(hookenv.local_unit())
        return conversation.get_remote(key)
