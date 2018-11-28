from sentry_policy_service import SentryPolicyService
from sentry_policy_service.ttypes import TCreateSentryRoleRequest, TListSentryRolesRequest

from thrift.protocol.TBinaryProtocol import TBinaryProtocol
from thrift.protocol.TMultiplexedProtocol import TMultiplexedProtocol
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TTransportException

from thrift_sasl import TSaslClientTransport

import sasl

class SentryClient(object):
    """

    Example usage::

        >>> from pysentry.client import SentryClient


    """

    SERVICE_NAME = 'SentryPolicyService'
    MECHANISM = 'GSSAPI'

    ERR_CONNECTION = 1

    def __init__(self, host, port='8038', service='sentry'):
        """
        'host'
        'port'
        'service'
        """
        self.host = host
        self.port = port
        self.service = service
        self.client = None

    def open(self):
        """
        Connect
        :return:
        """
        if self.client is not None:
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

                # self.protocol = TBinaryProtocol(self.transport)
                # TODO Test with MultiplexedProtocol
                self.protocol = TMultiplexedProtocol(TBinaryProtocol(self.transport), self.SERVICE_NAME)

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

    def create_role(self, user, role):
        req = TCreateSentryRoleRequest(requestorUserName=user, roleName=role)
        res = self.client.create_sentry_role(req)
        return res.status.value, res.status.message, None


class SentryError(Exception):
    def __init__(self, code, message, stack=None):
        self.code = code
        self.message = message
        self.stack = stack

    def __str__(self):
        return "(Code: {}) {}".format(self.code, self.message)

