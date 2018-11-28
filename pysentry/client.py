from sentry_policy_service import SentryPolicyService
from sentry_policy_service.ttypes import TListSentryRolesRequest

from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TTransportException

from thrift_sasl import TSaslClientTransport

import sasl

class SentryClient(object):
    """

    Example usage::

        >>> from pysentry.client import SentryClient


    """

    MECHANISM = 'GSSAPI'

    ERR_CONNECTION = 1

    def __init__(self, host, port, service='sentry'):
        """
        'host'
        'port'
        'service'
        """
        self.host = host
        self.port = port
        self.service = service

    def open(self):
        """
        Connect
        :return:
        """
        try:
            self.socket = TSocket(self.host, self.port)

            def sasl_factory():
                sasl_client = sasl.Client()
                sasl_client.setAttr('host', self.host)
                sasl_client.setAttr('service', self.service)
                sasl_client.init()
                return sasl_client

            self.transport = TSaslClientTransport(sasl_factory, self.MECHANISM, self.socket)
            self.transport.open()

            self.protocol = TBinaryProtocol(self.transport)

            self.client = SentryPolicyService.Client(self.protocol)
        except TTransportException as e:
            raise SentryError(self.ERR_CONNECTION, str(e))

    def close(self):
        """
        Disconnect
        :return:
        """
        try:
            self.transport.close()
            self.socket.close()
        except TTransportException as e:
            raise SentryError(self.ERR_CONNECTION, str(e))

    def list_roles_group(self, user, group=None):
        """
        List roles by group (or all groups)

        status {
            value
            message
        }
        roles {
            roleName
            groups {
                groupName
            }
        }

        :return:
        """
        req = TListSentryRolesRequest(requestorUserName=user, groupName=group)
        res = self.client.list_sentry_roles_by_group(req)
        return res.status.value, res.status.message, res.roles


class SentryError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "(Code: {}) {}".format(self.code, self.message)

