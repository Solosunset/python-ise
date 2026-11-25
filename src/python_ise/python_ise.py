"""Class to configure Cisco ISE via the ERS API."""

# Copyright (C) 2026 SoloSunset
# Derived from falkowich/ise.
#
# This file is part of python-ise and is free software: you can redistribute
# it and/or modify it under the terms of the GNU General Public License,
# version 2 only, as published by the Free Software Foundation.
#
# python-ise is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with python-ise. If not, see <https://www.gnu.org/licenses/>.

import json
import xmltodict
import re
from furl import furl
from datetime import datetime, timedelta
import asyncio
import aiohttp
import requests
from xml.parsers.expat import ExpatError
from .generated.ers_read import ERSGeneratedMethods

class InvalidMacAddress(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
    
class InvalidOID(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class MNT(object):
    def __init__(self, mnt_node: str, mnt_user: str, mnt_pass: str, verify=False, disable_warnings=False, use_csrf=False, timeout=5,
                 protocol='https'):
            """
            Class to interact with Cisco ISE via the MNT API.

            :param mnt_node: IP Address or hostname of a ISE MNT node
            :param mnt_user: MNT username
            :param mnt_pass: MNT password
            :param verify: Verify SSL cert
            :param disable_warnings: Disable requests warnings
            :param timeout: Query timeout
            """
            self.ise_node = mnt_node
            self.user_name = mnt_user
            self.user_pass = mnt_pass
            self.protocol = protocol

            self.url_base = '{0}://{1}/admin/API/mnt'.format(self.protocol, self.ise_node)
            self.ise = requests.sessions.Session()
            self.ise.auth = (self.user_name, self.user_pass)
            # http://docs.python-requests.org/en/latest/user/advanced/#ssl-cert-verification
            self.ise.verify = verify
            self.disable_warnings = disable_warnings
            self.use_csrf = use_csrf
            self.csrf = None
            self.csrf_expires = None
            self.timeout = timeout
            self.ise.headers.update({'Connection': 'keep_alive'})

            if self.disable_warnings:
                requests.packages.urllib3.disable_warnings()
    
    @staticmethod
    def _mac_test(mac: str) -> bool:
        """
        Test for valid mac address.

        :param mac: MAC address in the form of AA:BB:CC:00:11:22
        :return: True/False
        """
        
        mac_address_pattern = r"^(([0-9A-F]{2}(:|-)){5}[0-9A-F]{2}|([0-9A-F]{4}\.){2}[0-9A-F]{4}|[0-9A-F]{12})$"

        if mac and re.match(mac_address_pattern, mac.upper()):
            return True
        else:
            return False

    @staticmethod
    def _pass_mntresponse(result: dict, resp) -> dict:
        """
        Parse the MNT API error response.

        :param result: The result dictionary.
        :param resp: The response object.
        :return: The result dictionary with the error information.
        """
        result['error'] = resp.status_code
        try:
            result['response'] = xmltodict.parse(resp.text)
        except ExpatError:
            return result
        return result
            
    @staticmethod
    def _response_reader(response: str) -> dict:
        """
        Parse the response from the MNT API.

        :param response: The response from the MNT API.
        :return: A dictionary containing the parsed response.
        """
        data = response

        # Remove the enclosing curly braces and trailing space
        data = data.strip("{} ")

        # Split the string into key-value pairs
        pairs = data.split(";")

        # Initialize an empty dictionary
        result = {}

        # Iterate through each pair
        for pair in pairs:
            pair = pair.strip()
            if '=' in pair:
                key, value = pair.split("=", 1)
                # Handle repeated keys (e.g., cisco-av-pair)
                if key in result:
                    if isinstance(result[key], list):
                        result[key].append(value)
                    else:
                        result[key] = [result[key], value]
                else:
                    result[key] = value

        return result
    
    @staticmethod
    def _other_attr_string_reader(other_attr_string: str) -> dict:
        '''
        Converts other_attr_string from session to python dict

        :param other_attr_string: other_attr_string from ISE session
        :return: dict
        '''
        data = other_attr_string

        # Remove the leading and trailing delimiter and space
        data = data.strip(":!:")

        # Split the string into key-value pairs
        pairs = data.split(":!:")

        # Initialize an empty dictionary
        result = {}

        # Iterate through each pair
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split("=", 1)
                # Handle repeated keys
                if key in result:
                    if isinstance(result[key], list):
                        result[key].append(value)
                    else:
                        result[key] = [result[key], value]
                else:
                    result[key] = value

        # return the resulting dictionary
        return result
    
    def _get_object(self, url: str, objectid: str, objecttype: str):
        """
        Get a generic object from the MNT API.

        :param url: The URL to send the request to.
        :param objectid: The ID of the object to get.
        :param objecttype: The type of the object to get.
        :return: A dictionary containing the success status, response data, and error message.
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update(
            {'Accept': 'application/xml', 'Content-Type': 'application/xml'})

        f = furl(url)
        f.path /= objectid
        resp = self.ise.get(f.url)

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = xmltodict.parse(resp.content)[objecttype]
            return result
        else:
            return MNT._pass_mntresponse(result, resp)

    def get_activeCount(self) -> dict:
        """
        Get the number of active sessions.

        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/Session/ActiveCount', '', 'sessionCount')

        return result
    
    def get_postureCount(self) -> dict:
        """
        Get the number of postured endpoints.

        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/Session/PostureCount', '', 'sessionCount')

        return result

    def get_profilerCount(self) -> dict:
        """
        Get the number of active profiler service sessions.

        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/Session/ProfilerCount', '', 'sessionCount')

        return result
    
    def get_activeSessionList(self) -> dict:
        """
        Get a list of all active sessions.

        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/Session/ActiveList', '', 'activeList')

        if isinstance(result['response'], dict):
            sessions = result['response'].get('activeSession', [])
            result['response'] = sessions if isinstance(sessions, list) else [sessions]

        return result

    def get_authenticatedSessionsList(self, starttime='null', endtime='null') -> dict:
        """
        Get a list of all authenticated sessions.

        :param starttime: The start time of the session list.
        :param endtime: The end time of the session list.
        :return: A dictionary containing the success status, response data, and error message.
        """
        # TODO return error on incorrect timestamp
        """
        Lists all active sessions

        :param starttime str: 'YYYY-MM-DD hh:mm:ss'|'null'
        :param endtime str: 'YYYY-MM-DD hh:mm:ss'|'null'
        :return: result dictionary

        null/null Lists all active authenticated sessions.
        null/endtime Lists all active authenticated sessions after the specified end time.
        starttime/null Lists all active authenticated sessions before the specified start time.
        starttime/endtime Lists all active authenticated sessions between the specified start time and end time.
        """

        result = self._get_object(f'{self.url_base}/Session/AuthList/{starttime}/{endtime}', '', 'activeList')
        
        if isinstance(result['response'], dict):
            result['response'] = result['response'].get('activeSession', [])

        return result

    def get_session_macAddress(self, mac_address: str, convertOutputToDict=True) -> dict:
        """
        Get the active session of an endpoint by MAC address.

        :param mac_address: The MAC address of the endpoint.
        :param convertOutputToDict: Whether to convert the output to a dictionary.
        :return: A dictionary containing the success status, response data, and error message.
        """

        is_valid = MNT._mac_test(mac_address)

        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac_address))

        result = self._get_object(f'{self.url_base}/Session/MACAddress/', mac_address, 'sessionParameters')
        
        if not convertOutputToDict:
            return result

        if isinstance(result['response'], dict) and result['response'].get('other_attr_string'):
            result['response']['other_attr_string'] = \
                self._other_attr_string_reader(result['response']['other_attr_string'])

        return result
    
    def get_session_userName(self, user_name: str, convertOutputToDict=True) -> dict:
        """
        Get the active session of a user by username.

        :param user_name: The username of the user.
        :param convertOutputToDict: Whether to convert the output to a dictionary.
        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/Session/UserName/', user_name, 'sessionParameters')

        if not convertOutputToDict:
            return result

        if isinstance(result['response'], dict) and result['response'].get('other_attr_string'):
            result['response']['other_attr_string'] = \
                self._other_attr_string_reader(result['response']['other_attr_string'])

        return result
    
    def get_session_IPAddress(self, IPaddress: str, convertOutputToDict=True) -> dict:
        """
        Get the active session of an endpoint by IP address.

        :param IPaddress: The IP address of the endpoint.
        :param convertOutputToDict: Whether to convert the output to a dictionary.
        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/Session/IPAddress/', IPaddress, 'sessionParameters')

        if not convertOutputToDict:
            return result

        if isinstance(result['response'], dict) and result['response'].get('other_attr_string'):
            result['response']['other_attr_string'] = \
                self._other_attr_string_reader(result['response']['other_attr_string'])

        return result

    def get_session_ID(self, session_id: str, convertOutputToDict=True) -> dict:
        """
        Get the active session of an endpoint by session ID.

        :param session_id: The session ID of the endpoint.
        :param convertOutputToDict: Whether to convert the output to a dictionary.
        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/Session/Active/SessionID/{session_id}/0', '', 'activeSessionList')

        if not convertOutputToDict:
            return result

        # ActiveList is returned, maybe this needs to be reworked to allow for a list of sessions, though one would think an audit_session_id would only correspond with one session
        if isinstance(result['response'], dict) and result['response'].get('activeSession'):
            result['response'] = result['response']['activeSession']

        return result

    def get_version(self) -> dict:
        """
        Get the version of the MNT node.

        :return: A dictionary containing the success status, response data, and error message.
        """
        """
        Lists the node version and type
        0=STAND_ALONE_MNT_NODE
        1=ACTIVE_MNT_NODE
        2=STAND_BY_MNT_NODE
        3=NOT_AN_MNT_NODE

        :return: result dictionary
        """

        result = self._get_object(f'{self.url_base}/Version', '', 'product')

        return result
    
    def get_failureReasons(self) -> dict:
        """
        Get a list of failure reasons.

        :return: A dictionary containing the success status, response data, and error message.
        """

        result = self._get_object(f'{self.url_base}/FailureReasons', '', 'failureReasonList')

        return result

    def get_endpoint_authStatus(self, mac_address: str, seconds=3600, maxRecords=10, convertOutputToDict=True, convertTimestamps=False):
        """
        Get the authentication status of an endpoint.

        :param mac_address: The MAC address of the endpoint.
        :param seconds: The number of seconds to look back.
        :param maxRecords: The maximum number of records to return.
        :param convertOutputToDict: Whether to convert the output to a dictionary.
        :param convertTimestamps: Whether to convert timestamps to a human-readable format.
        :return: A dictionary containing the success status, response data, and error message.
        """

        is_valid = MNT._mac_test(mac_address)

        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac_address))

        result = self._get_object(f'{self.url_base}/AuthStatus/MACAddress/{mac_address}/{seconds}/{maxRecords}/All', '', 'authStatusOutputList')

        if not convertOutputToDict:
            return result

        # if response not dict return response
        if not isinstance(result['response'], dict):
            return result

        # if endpoint does not have session in the given timeperiod return
        if not result['response']['authStatusList'].get('authStatusElements'):
            return result

        # if authStatusElements is a dict, eg. there is only one session in the response, convert it to a list
        if isinstance(result['response']['authStatusList']['authStatusElements'], dict):
            result['response']['authStatusList']['authStatusElements'] = [result['response']['authStatusList']['authStatusElements']]
        
        # loop over authStatusElements and convert them to dicts
        for i in range(len(result['response']['authStatusList']['authStatusElements'])):

            # Convert acs_timestamp to human readable format
            if convertTimestamps:
                result['response']['authStatusList']['authStatusElements'][i]['acs_timestamp'] = \
                    datetime.strptime(
                        result['response']['authStatusList']['authStatusElements'][i]['acs_timestamp'], 
                        '%Y-%m-%dT%H:%M:%S.%f%z'
                    ).strftime("%H:%M:%S %d-%m-%Y")
            
            if result['response']['authStatusList']['authStatusElements'][i].get('response'):
                result['response']['authStatusList']['authStatusElements'][i]['response'] = \
                    self._response_reader(result['response']['authStatusList']['authStatusElements'][i]['response'])
        
            if result['response']['authStatusList']['authStatusElements'][i].get('other_attr_string'):
                result['response']['authStatusList']['authStatusElements'][i]['other_attr_string'] = \
                    self._other_attr_string_reader(result['response']['authStatusList']['authStatusElements'][i]['other_attr_string'])

        return result

    def get_acctStatus(self, mac_address: str, seconds=3600) -> dict:
        """
        Get the accounting status of an endpoint.

        :param mac_address: The MAC address of the endpoint.
        :param seconds: The number of seconds to look back.
        :return: A dictionary containing the success status, response data, and error message.
        """

        is_valid = MNT._mac_test(mac_address)

        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac_address))

        result = self._get_object(f'{self.url_base}/AcctStatusTT/MACAddress/{mac_address}/{seconds}', '', 'acctStatusOutputList')

        return result
    
    def get_CoA_reauth(self, server_hostname: str, mac_address: str, reauth_type: int, nas_ip_address=None, destination_ip_address=None) -> dict:
        """
        Send a CoA reauthentication request to an endpoint.

        :param server_hostname: The hostname of the server.
        :param mac_address: The MAC address of the endpoint.
        :param reauth_type: The type of reauthentication to perform.
        :param nas_ip_address: The IP address of the NAS.
        :param destination_ip_address: The destination IP address.
        :return: A dictionary containing the success status, response data, and error message.
        """

        is_valid = MNT._mac_test(mac_address)

        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac_address))

        url = f'{self.url_base}/CoA/Reauth/{server_hostname}/{mac_address}/{reauth_type}'

        if nas_ip_address and destination_ip_address:
            url += f'/{nas_ip_address}/{destination_ip_address}/'

        result = self._get_object(url, '', 'remoteCoA')

        return result

    def get_CoA_disconnect(self, server_hostname: str, mac_address: str, disconnect_type: int, nas_ip_address=None, destination_ip_address=None) -> dict:
        """
        Send a CoA disconnect request to an endpoint.

        :param server_hostname: The hostname of the server.
        :param mac_address: The MAC address of the endpoint.
        :param disconnect_type: The type of disconnect to perform.
        :param nas_ip_address: The IP address of the NAS.
        :param destination_ip_address: The destination IP address.
        :return: A dictionary containing the success status, response data, and error message.
        """

        is_valid = MNT._mac_test(mac_address)

        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac_address))

        url = f'{self.url_base}/CoA/Disconnect/{server_hostname}/{mac_address}/{disconnect_type}'

        if nas_ip_address and destination_ip_address:
            url += f'/{nas_ip_address}/{destination_ip_address}/'

        result = self._get_object(url, '', 'remoteCoA')

        return result

class ERS(ERSGeneratedMethods):
    def __init__(self, ise_node, ers_user, ers_pass, verify=False, disable_warnings=False, use_csrf=False, timeout=5,
                 protocol='https'):
        """
        Class to interact with Cisco ISE via the ERS API.

        :param ise_node: IP Address or hostname of the primary admin ISE node
        :param ers_user: ERS username
        :param ers_pass: ERS password
        :param verify: Verify SSL cert
        :param disable_warnings: Disable requests warnings
        :param timeout: Query timeout
        """
        self.ise_node = ise_node
        self.user_name = ers_user
        self.user_pass = ers_pass
        self.protocol = protocol

        self.url_base = '{0}://{1}:9060/ers'.format(self.protocol, self.ise_node)
        self.ise = requests.sessions.Session()
        self.ise.auth = (self.user_name, self.user_pass)
        # http://docs.python-requests.org/en/latest/user/advanced/#ssl-cert-verification
        self.ise.verify = verify
        self.disable_warnings = disable_warnings
        self.use_csrf = use_csrf
        self.csrf = None
        self.csrf_expires = None
        self.timeout = timeout
        self.ise.headers.update({'Connection': 'keep_alive'})

        if self.disable_warnings:
            requests.packages.urllib3.disable_warnings()

    @staticmethod
    def _mac_test(mac: str) -> bool:
        """
        Test for valid mac address.

        :param mac: MAC address in the form of AA:BB:CC:00:11:22
        :return: True/False
        """
        
        mac_address_pattern = r"^(([0-9A-F]{2}(:|-)){5}[0-9A-F]{2}|([0-9A-F]{4}\.){2}[0-9A-F]{4}|[0-9A-F]{12})$"

        if mac and re.match(mac_address_pattern, mac.upper()):
            return True
        else:
            return False

    @staticmethod
    def _sgt_name_test(name: str) -> bool:
        """
        Test for valid name.

        :param name: Name; must not be null, must be <= 32 char, alphanumeric + _ only.
        :return: True/False
        """
        if name and re.search(r'^[a-zA-Z0-9_]*$', name) is not None and len(name) <= 32:
            return True
        else:
            return False

    @staticmethod
    def _sgacl_name_test(name: str) -> bool:
        """
        Test for valid name.

        :param name: Name; must start with letter; alphanumeric + _ only.
        :return: True/False
        """
        if name and re.search(r'^[a-zA-Z][a-zA-Z0-9_]*$', name) is not None:
            return True
        else:
            return False

    @staticmethod
    def _oid_test(id: str) -> bool:
        """
        Test for a valid OID
        :param id: OID in the form of abcd1234-ef56-7890-abcd1234ef56
        :return: True/False
        """
        if id and re.match(r'^([a-f0-9]{8}-([a-f0-9]{4}-){3}[a-z0-9]{12})$', id):
            return True
        else:
            return False

    @staticmethod
    def _pass_ersresponse(result: dict, resp) -> dict:
        """
        In case of error in API call, parse error into response dict

        :param result: result dict from _get_object
        :param result: requests.request.session response
        :return: result dictionary
        """
        result['error'] = resp.status_code

        errors = {        
            400: 'Bad Request, presumably a problem with python-ise package',
            401: 'Forbidden, check that you are authorized and using correct username/password',
            403: 'Unauthorized, check that you are authorized and using correct username/password',
            404: 'Not Found',
            405: 'Method Not Allowed, presumably a problem with python-ise package',
            429: 'Too Many Requests (ratelimit), slow down',
            500: 'Internal Server Error, ISE failed to generate a response'
        }

        result['response'] = errors.get(resp.status_code, '')
        
        if resp.text:
            result['response'] += ' - ' + resp.text
        
        return result

    def _request(self, url, method="get", data=None):
        """
        Generic request method.
        """
        if self.use_csrf:
            clock = getattr(self, 'clock', datetime.utcnow)
            now = clock()
            if not self.csrf_expires or not self.csrf or now > self.csrf_expires:
                self.ise.headers.update({'ACCEPT': 'application/json', 'Content-Type': 'application/json',
                                         'X-CSRF-TOKEN': 'fetch'})

                resp = self.ise.get('{0}/config/deploymentinfo/versioninfo'.format(self.url_base))
                self.csrf = resp.headers["X-CSRF-Token"]
                self.csrf_expires = now + timedelta(seconds=60)

            self.ise.headers.update({'ACCEPT': 'application/json', 'Content-Type': 'application/json',
                                     'X-CSRF-TOKEN': self.csrf})

            req = self.ise.request(method, url, data=data, timeout=self.timeout)
        else:
            req = self.ise.request(method, url, data=data, timeout=self.timeout)

        return req

    def _bulk_request(self, url, payload):
        """
        Handles bulk requests.
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})
        resp = self._request(url, method='post', data=json.dumps(payload))
        if resp.status_code == 202:
            result['success'] = True
            result['response'] = resp.json()
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def _get_groups(self, url: str, filter: str = None, size: int = 20, page: int = 1):
        """
        Get generic group lists.

        :param url: Base URL for requesting lists
        :param size: size of the page to return. Default: 20
        :param page: page to return. Default: 1
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        f = furl(url)
        # TODO test for valid size 1<=x>=100
        f.args['size'] = size
        # TODO test for valid page number?
        f.args['page'] = page
        # TODO add filter validation
        if filter:
            f.args['filter'] = filter

        resp = self.ise.get(f.url)

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = [(i['name'], i['id'], i['description'])
                                  for i in resp.json()['SearchResult']['resources']]
            result['total'] = resp.json()['SearchResult']['total']
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def _get_object(self, url: str, objectid: str, objecttype: str):
        """
        Get generic object lists.

        :param url: Base URL for requesting lists
        :param objectid: ID retreved from previous search.
        :param objecttype: "ERSEndPoint", etc...
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update(
            {'Accept': 'application/json', 'Content-Type': 'application/json'})

        f = furl(url)
        f.path /= objectid
        resp = self.ise.get(f.url)

        if resp.status_code == 200:
            result['success'] = True
            try:
                result['response'] = resp.json()[objecttype]
            except KeyError:
                result['response'] = resp.json()[list(resp.json().keys())[0]]
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def _get_objects(self, url: str, filter: str|list = None, size: int = 20, page: int = 1) -> dict:
        """
        Generic method for requesting objects lists.

        :param url: Base URL for requesting lists
        :param filter: argument side of a ERS filter string. Default: None
        :param size: size of the page to return. Default: 20
        :param page: page to return. Default: 1
        :return: result dictionary
        """
        
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update(
            {'Accept': 'application/json', 'Content-Type': 'application/json'})

        f = furl(url)
        f.args['size'] = size
        f.args['page'] = page
        # TODO add filter validation
        if filter:
            f.args['filter'] = filter

        resp = self.ise.get(f.url)

        
        if resp.status_code == 200:
            json_resp = resp.json()['SearchResult']

            result['total'] = json_resp['total']
            result['success'] = True

            if int(json_resp['total']):
                if json_resp.get('nextPage'):
                    result['nextPage'] = json_resp['nextPage']['href'].split('=')[-1]
                if json_resp.get('previousPage'):
                    result['prev'] = json_resp['previousPage']['href'].split('=')[-1]
                result['response'] = json_resp['resources']
                return result

            else:
                result['response'] = []
                return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def _get_all_objects(self, url: str, filter: str|list = None) -> dict:
        """
        Generic method for requesting all objects from a list.

        :param url: Base URL for requesting lists
        :param filter: argument side of a ERS filter string. Default: None
        :return: result dictionary
        """
        result = {'success': False, 'response': [], 'error': '', 'total': 0}

        total = self._get_objects(url, size=1, filter=filter)['total']
        pages = max(1, -(-total // 100))

        params_list = []
        for i in range(1, pages + 1):
            params = {
                "page": i,
                "size": 100
            }
            params_list.append(params)
        
        semaphore = asyncio.Semaphore(15)

        async def sem_task(session, url, params, filter):
            async with semaphore:
                return await self._async_get_objects(session, url, params, filter=filter)

        async def main():
            async with aiohttp.ClientSession() as session:
                tasks = [
                    sem_task(session, url, params, filter)
                    for params in params_list
                ]
                responses = await asyncio.gather(*tasks)
            return responses

        responses = asyncio.run(main())
        
        for response in responses:
            result['response'].extend(response['response'])

        result['total'] = len(result['response'])

        result['success'] = True

        return result
    
    async def _async_get_objects(self, session, url, params, filter: str = None, size: int = 20, page: int = 1):
        """
        Generic asynchronous method for requesting objects lists.

        :param session: aiohttp client session
        :param url: Base URL for requesting lists
        :param params: Dictionary of parameters for the request
        :param filter: argument side of a ERS filter string. Default: None
        :param size: size of the page to return. Default: 20
        :param page: page to return. Default: 1
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        headers = dict(self.ise.headers)
        headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

        if filter:
            params['filter'] = filter
        
        async with session.get(url, params=params, auth=aiohttp.BasicAuth(self.user_name, self.user_pass), headers=headers) as resp:

            if resp.status == 200:
                json_res = await resp.json()

                json_res = json_res['SearchResult']

                if int(json_res['total']) >= 1:
                    result['success'] = True
                    if json_res.get('nextPage'):
                        result['nextPage'] = json_res['nextPage']['href'].split('=')[-1]
                    if json_res.get('previousPage'):
                        result['prev'] = json_res['previousPage']['href'].split('=')[-1]
                    result['total'] = json_res['total']
                    result['response'] = [(i['name'], i['id'])
                                        for i in json_res['resources']]
                    return result

                elif int(json_res['total']) == 0:
                    result['success'] = True
                    result['response'] = []
                    result['total'] = json_res['total']
                    return result
            else:
                result['error'] = resp.status
                result['response'] = await resp.text()
                return result

    def get_aciBindings(self) -> dict:
        """
        Get all ACI bindings.

        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/acibindings/getall', '', 'ACIBindings')

    def get_aciSettings(self) -> dict:
        """
        Get ACI settings.

        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/acisettings/', '', 'AciSettings')
    
    def get_egressMatrixCell_bulk(self, payload) -> dict:
        """
        Submit a bulk request for egress matrix cells.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/egressmatrixcell/bulk/submit', payload)

    def get_endpoint_rejectedEndpoints(self, size=100, page=1) -> dict:
        """
        Get all rejected endpoints.

        :param size: The number of items to return per page.
        :param page: The page number to return.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_objects(f'{self.url_base}/config/endpoint/rejectedendpoints', size=size, page=page)
    
    def get_endpoint_bulk(self, payload) -> dict:
        """
        Submit a bulk request for endpoints.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/endpoint/bulk/submit', payload)


    def get_identityGroup_name(self, name) -> dict:
        """
        Get an identity group by name.

        :param name: The name of the identity group.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/identitygroup/name', name, 'IdentityGroup')
    
    def get_identityGroup_id(self, OID) -> dict:
        """
        Get an identity group by ID.

        :param OID: The ID of the identity group.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/identitygroup', OID, 'IdentityGroup')
    
    def get_identityGroups(self, size=100, page=1) -> dict:
        """
        Get all identity groups.

        :param size: The number of items to return per page.
        :param page: The page number to return.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_objects(f'{self.url_base}/config/identitygroup', size=size, page=page)


    def get_internalUser_name(self, name) -> dict:
        """
        Get an internal user by name.

        :param name: The name of the internal user.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/internaluser/name', name, 'InternalUser')
    
    def get_internalUser_id(self, OID) -> dict:
        """
        Get an internal user by ID.

        :param OID: The ID of the internal user.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/internaluser', OID, 'InternalUser')
    
    def get_internalUsers(self, size=100, page=1) -> dict:
        """
        Get all internal users.

        :param size: The number of items to return per page.
        :param page: The page number to return.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_objects(f'{self.url_base}/config/internaluser', size=size, page=page)

    
    def get_ldap_rootCaCertificates(self, OID) -> dict:
        """
        Get the root CA certificates for an LDAP server.

        :param OID: The ID of the LDAP server.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/ldap/{OID}/getrootcacertificates', '', 'Ldap')

    def get_ldap(self, OID) -> dict:
        """
        Get an LDAP server by ID.

        :param OID: The ID of the LDAP server.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/ldap', OID, 'Ldap')
    
    def get_ldap_hosts(self, OID) -> dict:
        """
        Get the hosts for an LDAP server.

        :param OID: The ID of the LDAP server.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/ldap/{OID}/gethosts', '', 'Ldap')
    
    def get_ldap_issuerCertificates(self, OID) -> dict:
        """
        Get the issuer certificates for an LDAP server.

        :param OID: The ID of the LDAP server.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/ldap/{OID}/getissuercertificates', '', 'Ldap')
    
    def get_networkDevice_bulk(self, payload) -> dict:
        """
        Submit a bulk request for network devices.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/networkdevice/bulk/submit', payload)
    
    def get_sgacl_bulk(self, payload) -> dict:
        """
        Submit a bulk request for security group ACLs.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/sgacl/bulk/submit', payload)
    
    def get_sgMapping_bulk(self, payload) -> dict:
        """
        Submit a bulk request for security group mappings.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/sgmapping/bulk/submit', payload)
    
    def get_sgMappingGroup_bulk(self, payload) -> dict:
        """
        Submit a bulk request for security group mapping groups.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/sgmappinggroup/bulk/submit', payload)
    
    def get_sgtVnVlan_bulk(self, payload) -> dict:
        """
        Submit a bulk request for security group tag VN VLANs.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/sgtvnvlan/bulk/submit', payload)


    def get_sxpConnection_id(self, OID) -> dict:
        """
        Get an SXP connection by ID.

        :param OID: The ID of the SXP connection.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/sxpconnection', OID, 'SxpConnection')
    
    def get_sxpConnections(self, size=100, page=1) -> dict:
        """
        Get all SXP connections.

        :param size: The number of items to return per page.
        :param page: The page number to return.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_objects(f'{self.url_base}/config/sxpconnection', size=size, page=page)
    
    def get_sxpConnection_versionInfo(self) -> dict:
        """
        Get SXP connection version information.

        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/sxpconnection/versioninfo', '', 'VersionInfo')
    
    def get_sxpConnection_(self, OID) -> dict:
        """
        Get an SXP connection by ID.

        :param OID: The ID of the SXP connection.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/sxpconnection', OID, 'SxpConnection')

    def get_sxpLocalBinding_bulk(self, payload) -> dict:
        """
        Submit a bulk request for SXP local bindings.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/sxplocalbinding/bulk/submit', payload)


    def get_sxpVpn_id(self, OID) -> dict:
        """
        Get an SXP VPN by ID.

        :param OID: The ID of the SXP VPN.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/sxplocalbinding', OID, 'SxpVpn')
    
    def get_sxpVpns(self, size=100, page=1) -> dict:
        """
        Get all SXP VPNs.

        :param size: The number of items to return per page.
        :param page: The page number to return.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_objects(f'{self.url_base}/config/sxplocalbinding', size=size, page=page)

    def get_sxpVpn_versionInfo(self) -> dict:
        """
        Get SXP VPN version information.

        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._get_object(f'{self.url_base}/config/sxplocalbinding/versioninfo', '', 'VersionInfo')
    
    def get_sxpVpn_bulk(self, payload) -> dict:
        """
        Submit a bulk request for SXP VPNs.

        :param payload: The payload for the bulk request.
        :return: A dictionary containing the success status, response data, and error message.
        """
        return self._bulk_request(f'{self.url_base}/config/sxplocalbinding/bulk/submit', payload)

    def get_endpoint_groups(self, filter: str|list =None, size=20, page=1):
        """
        Get a list of endpoint identitygroups.

        :param filter: a filter like 'name.STARTSW.Test' or ['name.STARTSW.Test', 'name.ENDSW.Test2']
        :param size: 0-100 the amount of groups to get at once
        :param page: the page to get, if 40 groups exist and size=20 one would need to make 2 calls (page=1, page=2)
        :return: result dictionary
        """

        return self._get_objects('{0}/config/endpointgroup'.format(self.url_base), filter=filter, size=size, page=page)

    def get_endpoint_group(self, endpoint_group):
        """
        Get endpoint identity group details.

        :param group: Name or OID of the identity group
        :return: result dictionary
        """
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        # If it's a valid OID get by id, else get by name
        if self._oid_test(endpoint_group):
            result = self._get_object(
                f'{self.url_base}/config/endpointgroup',
                endpoint_group,
                'EndPointGroup'
            )
        else:
            result = self._get_object(f'{self.url_base}/config/endpointgroup/name', 
                endpoint_group,
                "EndPointGroup")
        return result

    async def async_get_all_endpoint_groups(self):
        """
        Get all identity groups.
        """

        total = self.get_endpoint_groups(size=1)['total']
        pages = max(1, -(-total // 100))

        params_list = []
        for i in range(1, pages + 1):
            params = {
                "page": i,
                "size": 100
            }
            params_list.append(params)
        
        semaphore = asyncio.Semaphore(15)

        async def sem_task(session, url, params):
            async with semaphore:
                return await self._async_get_objects(session, url, params)

        async with aiohttp.ClientSession() as session:
            tasks = [
                sem_task(session, f'{self.url_base}/config/endpointgroup', params)
                for params in params_list
            ]
            responses = await asyncio.gather(*tasks)

        return responses

    def get_all_endpoint_groups(self):
        responses = asyncio.run(self.async_get_all_endpoint_groups())
        
        return responses

    async def async_get_all_endpoints(self, groupID, staticGroup=True):
        """
        Get all endpoints in group.

        :param groupID: List only endpoints in a specific GroupID. Default: None
        :param staticGroup: List only endpoints in a statically assigned endpointGroup. Default: True
        :return: result dictionary
        """

        total = self.get_endpoints(f"groupId.EQ.{groupID}", size=1)['total']
        pages = max(1, -(-total // 100))

        filter = [f"groupId.EQ.{groupID}"]

        if staticGroup:
            filter.append("staticGroupAssignment.EQ.true")

        params_list = []
        for i in range(1, pages + 1):
            params = {
                "page": i,
                "size": 100
            }
            params_list.append(params)
        
        semaphore = asyncio.Semaphore(15)

        async def sem_task(session, url, params, filter):
            async with semaphore:
                return await self._async_get_objects(session, url, params, filter=filter)

        async with aiohttp.ClientSession() as session:
            tasks = [
                sem_task(session, f'{self.url_base}/config/endpoint', params, filter)
                for params in params_list
            ]
            responses = await asyncio.gather(*tasks)

        return responses

    def get_all_endpoints(self, groupID: str):
        """
        Get all endpoints in a specific group.

        :param groupID: The ID of the endpoint group.
        :return: A dictionary containing the success status, response data, error message, and total count.
        """
        
        result = {'success': False, 'response': [], 'error': '', 'total': 0}

        responses = asyncio.run(self.async_get_all_endpoints(groupID))

        for response in responses:
            result['response'].extend(response['response'])

        result['total'] = len(result['response'])

        result['success'] = True

        return result
    
    def get_sgt_search(self, sgt: str|int):
        """
        Get Scalable Group Tag details. Slower than get_sgt_id.

        :param sgt: name or number of a Scalable Group Tag
        :return: result dictionary
        """
        if isinstance(sgt, int):
            resp = self.get_sgts(filter=f'value.EQ.{sgt}')
        else:
            resp = self.get_sgts(filter=f'name.eq.{sgt}')
        
        if resp['total'] == 1:
            result = self.get_sgt_id(resp['response'][0]['id'])
            return result
        else:
            resp['response'] = 'Not Found'
            resp['error'] = 404
            resp['success'] = False
            return resp

    def add_sgt(self,
                name,
                description,
                value,
                propogate_to_apic=False,
                return_object=False):
        """
        Add a SGT to TrustSec Components

        :param name: Name
        :param description: Description
        :param value: SGT Number
        :param propogate_to_apic: Specific to ACI
        :param return_object: Look up object after creation and return in response
        """
        is_valid = ERS._sgt_name_test(name)
        if not is_valid:
            result = {
                'success': False,
                'response': '',
                'error': '{0}. Invalid Security Group name, name may not be null and longer than 32 characters and '
                'only contain the alphanumeric or underscore characters.'.format(name)
            }
            return result
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            data = {"Sgt": {'name': name, 'description': description, 'value': value,
                            'propogateToApic': propogate_to_apic}}

            resp = self._request('{0}/config/sgt'.format(self.url_base), method='post', data=json.dumps(data))
            if resp.status_code == 201:
                result['success'] = True
                if return_object:
                    result['response'] = self.get_sgt(name)["response"]
                else:
                    result['response'] = '{0} Added Successfully'.format(name)
                return result
            else:
                return ERS._pass_ersresponse(result, resp)

    def update_sgt(self,
                   sgt,
                   name,
                   description,
                   value,
                   propogate_to_apic=False,
                   return_object=False):
        """
        Update SGT in TrustSec Components

        :param sgt: Object ID of sgt
        :param name: Name
        :param description: Description
        :param value: SGT Number
        :param propogate_to_apic: Specific to ACI
        :param return_object: Look up object after update and return in response
        """
        is_valid = ERS._sgt_name_test(name)
        if not is_valid:
            result = {
                'success': False,
                'response': '',
                'error': '{0}. Invalid Security Group name, name may not be null and longer than 32 characters and '
                'only contain the alphanumeric or underscore characters.'.format(name)
            }
            return result
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            data = {"Sgt": {'name': name, 'description': description, 'value': value,
                            'propogateToApic': propogate_to_apic}}

            resp = self._request(('{0}/config/sgt/' + sgt).format(self.url_base), method='put', data=json.dumps(data))
            if resp.status_code == 200:
                result['success'] = True
                if return_object:
                    result['response'] = self.get_sgt(sgt)["response"]
                else:
                    result['response'] = resp.json()
                return result
            else:
                return ERS._pass_ersresponse(result, resp)

    def delete_sgt(self, sgt):
        """
        Delete SGT in TrustSec Components

        :param sgt: Object ID of sgt
        :return: Result dictionary
        """
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self._request('{0}/config/sgt/{1}'.format(self.url_base, sgt), method='delete')

        if resp.status_code == 204:
            result['success'] = True
            result['response'] = '{0} Deleted Successfully'.format(sgt)
            return result
        elif resp.status_code == 404:
            result['response'] = '{0} not found'.format(sgt)
            result['error'] = resp.status_code
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def get_sgacl_search(self, sgacl: str):
        """
        Get Scalable Group ACL details. Slower than get_sgt_id.

        :param sgacl: name of a Scalable Group Tag
        :return: result dictionary
        """

        resp = self.get_sgacls(filter=f'name.eq.{sgacl}')
        
        if resp['total'] == 1:
            result = self.get_sgacl_id(resp['response'][0]['id'])
            return result
        else:
            resp['response'] = 'Not Found'
            resp['error'] = 404
            resp['success'] = False
            return resp

    def add_sgacl(self,
                  name,
                  description,
                  ip_version,
                  acl_content,
                  return_object=False):
        """
        Add a SG ACL to TrustSec Components

        :param name: Name
        :param description: Description
        :param ip_version: IPV4, IPV6, or IP_AGNOSTIC
        :param acl_content: List of ACLs
        :param return_object: Look up object after creation and return in response
        """
        is_valid = ERS._sgacl_name_test(name)
        if not is_valid:
            result = {
                'success': False,
                'response': '',
                'error': '{0}. Invalid SGACL name, name should start with a letter and can only contain the '
                         'alphanumeric or underscore characters.'.format(name)
            }
            return result
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            data = {"Sgacl": {'name': name, 'description': description, 'ipVersion': ip_version,
                              'aclcontent': "\n".join(acl_content)}}

            resp = self._request('{0}/config/sgacl'.format(self.url_base), method='post', data=json.dumps(data))
            if resp.status_code == 201:
                result['success'] = True
                if return_object:
                    result['response'] = self.get_sgacl(name)["response"]
                else:
                    result['response'] = '{0} Added Successfully'.format(name)
                return result
            else:
                return ERS._pass_ersresponse(result, resp)

    def update_sgacl(self,
                     sgacl,
                     name,
                     description,
                     ip_version,
                     acl_content,
                     return_object=False):
        """
        Update a SG ACL from TrustSec Components

        :param sgacl: Object ID of sgacl
        :param name: Name
        :param description: Description
        :param ip_version: IPV4, IPV6, or IP_AGNOSTIC
        :param acl_content: List of ACLs
        :param return_object: Look up object after creation and return in response
        """
        is_valid = ERS._sgacl_name_test(name)
        if not is_valid:
            result = {
                'success': False,
                'response': '',
                'error': '{0}. Invalid SGACL name, name should start with a letter and can only contain the '
                         'alphanumeric or underscore characters.'.format(name)
            }
            return result
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            data = {"Sgacl": {'name': name, 'description': description, 'ipVersion': ip_version,
                              'aclcontent': "\n".join(acl_content)}}

            resp = self._request(('{0}/config/sgacl/' + sgacl).format(self.url_base), method='put',
                                 data=json.dumps(data))
            if resp.status_code == 200:
                result['success'] = True
                if return_object:
                    result['response'] = self.get_sgacl(sgacl)["response"]
                else:
                    result['response'] = resp.json()
                return result
            else:
                return ERS._pass_ersresponse(result, resp)

    def delete_sgacl(self, sgacl):
        """
        Delete SGACL in TrustSec Components

        :param sgacl: Object ID of sgacl
        :return: Result dictionary
        """
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self._request('{0}/config/sgacl/{1}'.format(self.url_base, sgacl), method='delete')

        if resp.status_code == 204:
            result['success'] = True
            result['response'] = '{0} Deleted Successfully'.format(sgacl)
            return result
        elif resp.status_code == 404:
            result['response'] = '{0} not found'.format(sgacl)
            result['error'] = resp.status_code
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def get_egressmatrixcell(self, emc='', src_sgt=None, dst_sgt=None):
        """
        Get TrustSec Egress Matrix Cell Policy details. Both src_sgt and dst_sgt required if either is used.

        :param emc: description or Object ID of the TrustSec Egress Matrix Cell Policy
        :param src_sgt: name or Object ID of the Source SGT in the Policy
        :param src_sgt: name or Object ID of the Dest SGT in the Policy
        :return: result dictionary
        """

        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        # If it's a valid OID, perform a more direct GET-call
        if self._oid_test(emc):
            result = self._get_object(
                '{0}/config/egressmatrixcell'.format(self.url_base),
                emc,
                'EgressMatrixCell'
            )
            return result
        # If not valid OID, perform regular search
        else:
            if emc:
                resp = self.ise.get(
                    '{0}/config/egressmatrixcell?filter=description.EQ.{1}'.format(
                        self.url_base, emc))
                found_group = resp.json()
            elif src_sgt and dst_sgt:
                srcsgtval = self.get_sgt(src_sgt)["response"]["value"]
                dstsgtval = self.get_sgt(dst_sgt)["response"]["value"]
                resp = self.ise.get(
                    '{0}/config/egressmatrixcell?filter=sgtSrcValue.EQ.{1}&filter=sgtDstValue.EQ.{2}'.format(
                        self.url_base, srcsgtval, dstsgtval))
                found_group = resp.json()
            else:
                return result

        if found_group['SearchResult']['total'] == 1:
            result = self._get_object('{0}/config/egressmatrixcell'.format(self.url_base),
                                     found_group['SearchResult']['resources'][0]['id'], "EgressMatrixCell")

            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def add_egressmatrixcell(self,
                             source_sgt,
                             destination_sgt,
                             default_rule,
                             acls=None,
                             description=None,
                             return_object=False):
        """
        Add TrustSec Egress Matrix Cell Policy.

        :param description: Description
        :param source_sgt: Source SGT name or Object ID
        :param destination_sgt: Destination SGT name or Object ID
        :param default_rule: "NONE", "PERMIT_IP", "DENY_IP"
        :param acls: list of SGACL Object IDs. Can be None.
        :param return_object: Look up object after creation and return in response
        """

        # ISE will actually allow you to post duplicate polices, so before we execute the post, double check to
        # make sure a policy doesn't already exist
        src_sgt = self.get_sgt(source_sgt)["response"].get("id", None)
        dst_sgt = self.get_sgt(destination_sgt)["response"].get("id", None)
        if src_sgt and dst_sgt:
            celldata = self.get_egressmatrixcell(None, src_sgt=src_sgt, dst_sgt=dst_sgt)["response"]
        else:
            celldata = None

        if celldata:
            result = {
                'success': False,
                'response': '',
                'error': 'There is already a policy present for this source and destination. Please use update to make '
                         'policy changes.'
            }
            return result
        elif default_rule == "NONE" and acls is None:
            result = {
                'success': False,
                'response': '',
                'error': 'You must specify one or more acls as a list, or a default_rule; both cannot be blank'
            }
            return result
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            newacls = []
            if acls:
                for a in acls:
                    if self._oid_test(a):
                        newacls.append(a)
                    else:
                        newacl = self.get_sgacl(a)["response"].get("id", None)
                        if newacl:
                            newacls.append(newacl)

            data = {"EgressMatrixCell": {'description': description,
                                         'sourceSgtId': src_sgt,
                                         'destinationSgtId': dst_sgt,
                                         'defaultRule': default_rule, "matrixCellStatus": "ENABLED",
                                         'sgacls': newacls}}

            resp = self._request('{0}/config/egressmatrixcell'.format(self.url_base), method='post',
                                 data=json.dumps(data))
            if resp.status_code == 201:
                result['success'] = True
                if return_object:
                    result['response'] = self.get_egressmatrixcell(None, src_sgt=src_sgt, dst_sgt=dst_sgt)["response"]
                else:
                    result['response'] = '{0} Added Successfully'.format(description)
                return result
            else:
                return ERS._pass_ersresponse(result, resp)

    def update_egressmatrixcell(self,
                                emc,
                                source_sgt,
                                destination_sgt,
                                default_rule,
                                acls=None,
                                description=None,
                                return_object=False):
        """
        Update TrustSec Egress Matrix Cell Policy.

        :param emc: Object ID of egress matrix cell
        :param description: Description
        :param source_sgt: Source SGT name or Object ID
        :param destination_sgt: Destination SGT name or Object ID
        :param default_rule: "NONE", "PERMIT_IP", "DENY_IP"
        :param acls: list of SGACL Object IDs. Can be None.
        :param return_object: Look up object after creation and return in response
        """
        if not emc:
            result = {
                'success': False,
                'response': '',
                'error': 'You must provide the egress matrix cell object id in order to update it.'
            }
            return result
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            newacls = []
            if acls:
                for a in acls:
                    if self._oid_test(a):
                        newacls.append(a)
                    else:
                        newacl = self.get_sgacl(a)["response"].get("id", None)
                        if newacl:
                            newacls.append(newacl)

            src_sgt = self.get_sgt(source_sgt)["response"]["id"]
            dst_sgt = self.get_sgt(destination_sgt)["response"]["id"]
            data = {"EgressMatrixCell": {'id': emc, 'description': description,
                                         'sourceSgtId': src_sgt,
                                         'destinationSgtId': dst_sgt,
                                         'defaultRule': default_rule, "matrixCellStatus": "ENABLED",
                                         'sgacls': newacls}}

            resp = self._request(('{0}/config/egressmatrixcell/' + emc).format(self.url_base), method='put',
                                 data=json.dumps(data))
            if resp.status_code == 200:
                result['success'] = True
                if return_object:
                    result['response'] = self.get_egressmatrixcell(emc)["response"]
                else:
                    result['response'] = resp.json()
                return result
            else:
                return ERS._pass_ersresponse(result, resp)

    def delete_egressmatrixcell(self, emc):
        """
        Delete TrustSec Egress Matrix Cell Policy.

        :param emc: Object ID of egress matrix cell policy
        :return: Result dictionary
        """
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self._request('{0}/config/egressmatrixcell/{1}'.format(self.url_base, emc), method='delete')

        if resp.status_code == 204:
            result['success'] = True
            result['response'] = '{0} Deleted Successfully'.format(emc)
            return result
        elif resp.status_code == 404:
            result['response'] = '{0} not found'.format(emc)
            result['error'] = resp.status_code
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def get_endpoint_macAddress(self, mac_address):
        """
        Get endpoint details.

        :param mac_address: MAC address of the endpoint
        :return: result dictionary
        """

        is_valid = ERS._mac_test(mac_address)

        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac_address))

        result = self._get_object(
            f'{self.url_base}/config/endpoint/name/', 
            mac_address, 
            'ERSEndPoint'
        )
        return result

    def add_endpoint(self,
                     name,
                     mac,
                     group_id,
                     static_profile_assigment='false',
                     static_group_assignment='true',
                     profile_id='',
                     description='',
                     portalUser='',
                     customAttributes={}):
        """
        Add a user to the local user store.

        :param name: Name
        :param mac: Macaddress
        :param group_id: OID of group to add endpoint in
        :param static_profile_assigment: Set static profile
        :param static_group_assignment: Set static group
        :param profile_id: OID of profile
        :param description: User description
        :param portaluser: Portal username
        :param customAttributes: key value pairs of custom attributes
        :return: result dictionary
        """
        is_valid = ERS._mac_test(mac)
        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac))
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            data = {"ERSEndPoint": {'name': name, 'description': description, 'mac': mac,
                                    'profileId': profile_id, 'staticProfileAssignment': static_profile_assigment,
                                    'groupId': group_id, 'staticGroupAssignment': static_group_assignment,
                                    'portalUser': portalUser, 'customAttributes': {'customAttributes': customAttributes}
                                    }
                    }

            resp = self._request('{0}/config/endpoint'.format(self.url_base), method='post',
                                 data=json.dumps(data))
            if resp.status_code == 201:
                result['success'] = True
                result['response'] = '{0} Added Successfully'.format(name)
                return result
            else:
                return ERS._pass_ersresponse(result, resp)
    
    def update_endpoint(self,
                    uuid,
                    name,
                    mac,
                    group_id,
                    static_profile_assigment='false',
                    static_group_assignment='true',
                    profile_id='',
                    description='',
                    portalUser='',
                    customAttributes={}):
        """
        Update SGT in TrustSec Components

        :param sgt: Object ID of sgt
        :param name: Name
        :param description: Description
        :param value: SGT Number
        :param propogate_to_apic: Specific to ACI
        :param return_object: Look up object after update and return in response
        """
        is_valid = ERS._mac_test(mac)
        if not is_valid:
            raise InvalidMacAddress(
                '{0}. Must be in the form of AA:BB:CC:00:11:22'.format(mac))
        else:
            self.ise.headers.update(
                {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

            result = {
                'success': False,
                'response': '',
                'error': '',
            }

            data = {"ERSEndPoint": {'name': name, 'description': description, 'mac': mac,
                        'profileId': profile_id, 'staticProfileAssignment': static_profile_assigment,
                        'groupId': group_id, 'staticGroupAssignment': static_group_assignment,
                        'portalUser': portalUser, 'customAttributes': {'customAttributes': customAttributes}
                        }
                    }

            resp = self._request('{0}/config/endpoint/{1}'.format(self.url_base, uuid), method='put',
                        data=json.dumps(data))

            if resp.status_code == 200:
                result['success'] = True
                result['response'] = '{0} Updated Successfully'.format(name)
                return result
            else:
                return ERS._pass_ersresponse(result, resp)

    def delete_endpoint(self, mac):
        """
        Delete an endpoint.

        :param mac: Endpoint Macaddress
        :return: Result dictionary
        """
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self.ise.get(
            '{0}/config/endpoint?filter=mac.EQ.{1}'.format(self.url_base, mac))
        found_endpoint = resp.json()
        if found_endpoint['SearchResult']['total'] == 1:
            endpoint_oid = found_endpoint['SearchResult']['resources'][0]['id']
            resp = self._request(
                '{0}/config/endpoint/{1}'.format(self.url_base, endpoint_oid), method='delete')

            if resp.status_code == 204:
                result['success'] = True
                result['response'] = '{0} Deleted Successfully'.format(mac)
                return result
            elif resp.status_code == 404:
                result['response'] = '{0} not found'.format(mac)
                result['error'] = resp.status_code
                return result
            else:
                return ERS._pass_ersresponse(result, resp)
        elif found_endpoint['SearchResult']['total'] == 0:
            result['response'] = '{0} not found'.format(mac)
            result['error'] = 404
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def add_user(self,
                 user_id,
                 password,
                 user_group_oid,
                 enable='',
                 first_name='',
                 last_name='',
                 email='',
                 description=''):
        """
        Add a user to the local user store.

        :param user_id: User ID
        :param password: User password
        :param user_group_oid: OID of group to add user to
        :param enable: Enable password used for Tacacs
        :param first_name: First name
        :param last_name: Last name
        :param email: email address
        :param description: User description
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        data = {"InternalUser": {'name': user_id, 'password': password, 'enablePassword': enable,
                                 'firstName': first_name, 'lastName': last_name, 'email': email,
                                 'description': description, 'identityGroups': user_group_oid}}

        resp = self._request('{0}/config/internaluser'.format(self.url_base), method='post',
                             data=json.dumps(data))
        if resp.status_code == 201:
            result['success'] = True
            result['response'] = '{0} Added Successfully'.format(user_id)
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def delete_user(self, user_id):
        """
        Delete a user.

        :param user_id: User ID
        :return: Result dictionary
        """
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self.ise.get(
            '{0}/config/internaluser?filter=name.EQ.{1}'.format(self.url_base, user_id))
        found_user = resp.json()

        if found_user['SearchResult']['total'] == 1:
            user_oid = found_user['SearchResult']['resources'][0]['id']
            resp = self._request(
                '{0}/config/internaluser/{1}'.format(self.url_base, user_oid), method='delete')

            if resp.status_code == 204:
                result['success'] = True
                result['response'] = '{0} Deleted Successfully'.format(user_id)
                return result
            elif resp.status_code == 404:
                result['response'] = '{0} not found'.format(user_id)
                result['error'] = resp.status_code
                return result
            else:
                return ERS._pass_ersresponse(result, resp)
        elif found_user['SearchResult']['total'] == 0:
            result['response'] = '{0} not found'.format(user_id)
            result['error'] = 404
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def add_device(self,
                   name,
                   ip_address,
                   radius_key,
                   snmp_ro,
                   dev_group,
                   dev_location,
                   dev_type,
                   description='',
                   snmp_v='TWO_C',
                   dev_profile='Cisco',
                   tacacs_shared_secret=None,
                   tacas_connect_mode_options='ON_LEGACY'
                   ):
        """
        Add a device.

        :param name: name of device
        :param ip_address: IP address of device
        :param radius_key: Radius shared secret
        :param snmp_ro: SNMP read only community string
        :param dev_group: Device group name
        :param dev_location: Device location
        :param dev_type: Device type
        :param description: Device description
        :param dev_profile: Device profile
        :return: Result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        data = {'NetworkDevice': {'name': name,
                                  'description': description,
                                  'authenticationSettings': {
                                      'networkProtocol': 'RADIUS',
                                      'radiusSharedSecret': radius_key,
                                      'enableKeyWrap': 'false',
                                  },
                                  'snmpsettings': {
                                      'version': 'TWO_C',
                                      'roCommunity': snmp_ro,
                                      'pollingInterval': 3600,
                                      'linkTrapQuery': 'true',
                                      'macTrapQuery': 'true',
                                      'originatingPolicyServicesNode': 'Auto'
                                  },
                                  'profileName': dev_profile,
                                  'coaPort': 1700,
                                  'NetworkDeviceIPList': [{
                                      'ipaddress': ip_address,
                                      'mask': 32
                                  }],
                                  'NetworkDeviceGroupList': [
                                      dev_group, dev_type, dev_location,
                                      'IPSEC#Is IPSEC Device#No'
                                    ]
                                  }
                }

        if tacacs_shared_secret is not None:
            data['NetworkDevice']['tacacsSettings'] = {
              'sharedSecret': tacacs_shared_secret,
              'connectModeOptions': tacas_connect_mode_options
            }

        resp = self._request('{0}/config/networkdevice'.format(self.url_base), method='post',
                             data=json.dumps(data))

        if resp.status_code == 201:
            result['success'] = True
            result['response'] = '{0} Added Successfully'.format(name)
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

    def delete_device(self, device):
        """
        Delete a device.

        :param device: device_name
        :return: Result dictionary
        """
        self.ise.headers.update(
            {'ACCEPT': 'application/json', 'Content-Type': 'application/json'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self.ise.get(
            '{0}/config/networkdevice?filter=name.EQ.{1}'.format(self.url_base, device))
        found_device = resp.json()
        if found_device['SearchResult']['total'] == 1:
            device_oid = found_device['SearchResult']['resources'][0]['id']
            resp = self._request(
                '{0}/config/networkdevice/{1}'.format(self.url_base, device_oid), method='delete')

            if resp.status_code == 204:
                result['success'] = True
                result['response'] = '{0} Deleted Successfully'.format(device)
                return result
            elif resp.status_code == 404:
                result['response'] = '{0} not found'.format(device)
                result['error'] = resp.status_code
                return result
            else:
                return ERS._pass_ersresponse(result, resp)
        elif found_device['SearchResult']['total'] == 0:
            result['response'] = '{0} not found'.format(device)
            result['error'] = 404
            return result
        else:
            return ERS._pass_ersresponse(result, resp)

class OPENapi(object):
    def __init__():
        pass
