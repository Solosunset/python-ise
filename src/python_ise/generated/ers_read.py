"""Generated ERS read methods. Do not edit; run python -m python_ise.generate."""

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

class ERSGeneratedMethods:
    def get_acibinding_versionInfo(self) -> dict:
        """Get aciBindings version information."""
        return self._get_object(
            f'{self.url_base}/config/acibindings/versioninfo',
            '',
            'VersionInfo',
        )

    def get_aciSettings_versionInfo(self) -> dict:
        """Get aciSettings version information."""
        return self._get_object(
            f'{self.url_base}/config/acisettings/versioninfo',
            '',
            'VersionInfo',
        )

    def get_activeDirectories(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List activeDirectory resources."""
        return self._get_objects(
            f'{self.url_base}/config/activedirectory',
            filter=filter,
            size=size,
            page=page,
        )

    def get_activeDirectory_id(self, OID) -> dict:
        """Get a activeDirectory resource by id."""
        return self._get_object(
            f'{self.url_base}/config/activedirectory',
            OID,
            'ERSActiveDirectory',
        )

    def get_activeDirectory_name(self, name) -> dict:
        """Get a activeDirectory resource by name."""
        return self._get_object(
            f'{self.url_base}/config/activedirectory/name',
            name,
            'ERSActiveDirectory',
        )

    def get_activeDirectory_versionInfo(self) -> dict:
        """Get activeDirectory version information."""
        return self._get_object(
            f'{self.url_base}/config/activedirectory/versioninfo',
            '',
            'VersionInfo',
        )

    def get_adminusers(self, filter: str | list = None, size=20, page=1) -> dict:
        """List adminuser resources."""
        return self._get_objects(
            f'{self.url_base}/config/adminuser',
            filter=filter,
            size=size,
            page=page,
        )

    def get_adminuser_id(self, OID) -> dict:
        """Get a adminuser resource by id."""
        return self._get_object(
            f'{self.url_base}/config/adminuser',
            OID,
            'AdminUser',
        )

    def get_adminuser_versionInfo(self) -> dict:
        """Get adminuser version information."""
        return self._get_object(
            f'{self.url_base}/config/adminuser/versioninfo',
            '',
            'VersionInfo',
        )

    def get_allowedProtocols(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List allowedProtocol resources."""
        return self._get_objects(
            f'{self.url_base}/config/allowedprotocols',
            filter=filter,
            size=size,
            page=page,
        )

    def get_allowedProtocol_id(self, OID) -> dict:
        """Get a allowedProtocol resource by id."""
        return self._get_object(
            f'{self.url_base}/config/allowedprotocols',
            OID,
            'AllowedProtocols',
        )

    def get_allowedProtocol_name(self, name) -> dict:
        """Get a allowedProtocol resource by name."""
        return self._get_object(
            f'{self.url_base}/config/allowedprotocols/name',
            name,
            'AllowedProtocols',
        )

    def get_allowedProtocol_versionInfo(self) -> dict:
        """Get allowedProtocol version information."""
        return self._get_object(
            f'{self.url_base}/config/allowedprotocols/versioninfo',
            '',
            'VersionInfo',
        )

    def get_authorizationProfiles(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List authorizationProfile resources."""
        return self._get_objects(
            f'{self.url_base}/config/authorizationprofile',
            filter=filter,
            size=size,
            page=page,
        )

    def get_authorizationProfile_id(self, OID) -> dict:
        """Get a authorizationProfile resource by id."""
        return self._get_object(
            f'{self.url_base}/config/authorizationprofile',
            OID,
            'AuthorizationProfile',
        )

    def get_authorizationProfile_name(self, name) -> dict:
        """Get a authorizationProfile resource by name."""
        return self._get_object(
            f'{self.url_base}/config/authorizationprofile/name',
            name,
            'AuthorizationProfile',
        )

    def get_authorizationProfile_versionInfo(self) -> dict:
        """Get authorizationProfile version information."""
        return self._get_object(
            f'{self.url_base}/config/authorizationprofile/versioninfo',
            '',
            'VersionInfo',
        )

    def get_byodPortals(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List byodPortal resources."""
        return self._get_objects(
            f'{self.url_base}/config/byodportal',
            filter=filter,
            size=size,
            page=page,
        )

    def get_byodPortal_id(self, OID) -> dict:
        """Get a byodPortal resource by id."""
        return self._get_object(
            f'{self.url_base}/config/byodportal',
            OID,
            'BYODPortal',
        )

    def get_byodPortal_versionInfo(self) -> dict:
        """Get byodPortal version information."""
        return self._get_object(
            f'{self.url_base}/config/byodportal/versioninfo',
            '',
            'VersionInfo',
        )

    def get_certificateProfiles(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List certificateProfile resources."""
        return self._get_objects(
            f'{self.url_base}/config/certificateprofile',
            filter=filter,
            size=size,
            page=page,
        )

    def get_certificateProfile_id(self, OID) -> dict:
        """Get a certificateProfile resource by id."""
        return self._get_object(
            f'{self.url_base}/config/certificateprofile',
            OID,
            'CertificateProfile',
        )

    def get_certificateProfile_versionInfo(self) -> dict:
        """Get certificateProfile version information."""
        return self._get_object(
            f'{self.url_base}/config/certificateprofile/versioninfo',
            '',
            'VersionInfo',
        )

    def get_certificateTemplates(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List certificateTemplate resources."""
        return self._get_objects(
            f'{self.url_base}/config/certificatetemplate',
            filter=filter,
            size=size,
            page=page,
        )

    def get_certificateTemplate_id(self, OID) -> dict:
        """Get a certificateTemplate resource by id."""
        return self._get_object(
            f'{self.url_base}/config/certificatetemplate',
            OID,
            'ERSCertificateTemplate',
        )

    def get_certificateTemplate_name(self, name) -> dict:
        """Get a certificateTemplate resource by name."""
        return self._get_object(
            f'{self.url_base}/config/certificatetemplate/name',
            name,
            'ERSCertificateTemplate',
        )

    def get_certificateTemplate_versionInfo(self) -> dict:
        """Get certificateTemplate version information."""
        return self._get_object(
            f'{self.url_base}/config/certificatetemplate/versioninfo',
            '',
            'VersionInfo',
        )

    def get_downloadableACLs(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List downloadableACL resources."""
        return self._get_objects(
            f'{self.url_base}/config/downloadableacl',
            filter=filter,
            size=size,
            page=page,
        )

    def get_downloadableACL_id(self, OID) -> dict:
        """Get a downloadableACL resource by id."""
        return self._get_object(
            f'{self.url_base}/config/downloadableacl',
            OID,
            'DownloadableAcl',
        )

    def get_downloadableACL_versionInfo(self) -> dict:
        """Get downloadableACL version information."""
        return self._get_object(
            f'{self.url_base}/config/downloadableacl/versioninfo',
            '',
            'VersionInfo',
        )

    def get_egressmatrixcells(self, filter: str | list = None, size=20, page=1) -> dict:
        """List egressmatrixcell resources."""
        return self._get_objects(
            f'{self.url_base}/config/egressmatrixcell',
            filter=filter,
            size=size,
            page=page,
        )

    def get_egressmatrixcell_id(self, OID) -> dict:
        """Get a egressmatrixcell resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/egressmatrixcell',
            OID,
            'EgressMatrixCell',
        )

    def get_egressMatrixCell_versionInfo(self) -> dict:
        """Get egressmatrixcell version information."""
        return self._get_object(
            f'{self.url_base}/config/egressmatrixcell/versioninfo',
            '',
            'VersionInfo',
        )

    def get_endpoints(self, filter: str | list = None, size=20, page=1) -> dict:
        """List endpoint resources."""
        return self._get_objects(
            f'{self.url_base}/config/endpoint',
            filter=filter,
            size=size,
            page=page,
        )

    def get_endpoint_id(self, OID) -> dict:
        """Get a endpoint resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/endpoint',
            OID,
            'ERSEndPoint',
        )

    def get_endpoint_name(self, name) -> dict:
        """Get a endpoint resource by name."""
        return self._get_object(
            f'{self.url_base}/config/endpoint/name',
            name,
            'ERSEndPoint',
        )

    def get_endpoint_versionInfo(self) -> dict:
        """Get endpoint version information."""
        return self._get_object(
            f'{self.url_base}/config/endpoint/versioninfo',
            '',
            'VersionInfo',
        )

    def get_endpointCert_versionInfo(self) -> dict:
        """Get endpointCert version information."""
        return self._get_object(
            f'{self.url_base}/config/endpointcert/versioninfo',
            '',
            'VersionInfo',
        )

    def get_endpointGroups(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List endpointGroup resources."""
        return self._get_objects(
            f'{self.url_base}/config/endpointgroup',
            filter=filter,
            size=size,
            page=page,
        )

    def get_endpointGroup_id(self, OID) -> dict:
        """Get a endpointGroup resource by id."""
        return self._get_object(
            f'{self.url_base}/config/endpointgroup',
            OID,
            'EndPointGroup',
        )

    def get_endpointGroup_name(self, name) -> dict:
        """Get a endpointGroup resource by name."""
        return self._get_object(
            f'{self.url_base}/config/endpointgroup/name',
            name,
            'EndPointGroup',
        )

    def get_endpointGroup_versionInfo(self) -> dict:
        """Get endpointGroup version information."""
        return self._get_object(
            f'{self.url_base}/config/endpointgroup/versioninfo',
            '',
            'VersionInfo',
        )

    def get_externalRadiusServers(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List externalRadiusServer resources."""
        return self._get_objects(
            f'{self.url_base}/config/externalradiusserver',
            filter=filter,
            size=size,
            page=page,
        )

    def get_externalRadiusServer_id(self, OID) -> dict:
        """Get a externalRadiusServer resource by id."""
        return self._get_object(
            f'{self.url_base}/config/externalradiusserver',
            OID,
            'ExternalRadiusServer',
        )

    def get_externalRadiusServer_name(self, name) -> dict:
        """Get a externalRadiusServer resource by name."""
        return self._get_object(
            f'{self.url_base}/config/externalradiusserver/name',
            name,
            'ExternalRadiusServer',
        )

    def get_externalRadiusServer_versionInfo(self) -> dict:
        """Get externalRadiusServer version information."""
        return self._get_object(
            f'{self.url_base}/config/externalradiusserver/versioninfo',
            '',
            'VersionInfo',
        )

    def get_filterPolicies(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List filterPolicy resources."""
        return self._get_objects(
            f'{self.url_base}/config/filterpolicy',
            filter=filter,
            size=size,
            page=page,
        )

    def get_filterPolicy_id(self, OID) -> dict:
        """Get a filterPolicy resource by id."""
        return self._get_object(
            f'{self.url_base}/config/filterpolicy',
            OID,
            'FilterPolicy',
        )

    def get_filterPolicy_versionInfo(self) -> dict:
        """Get filterPolicy version information."""
        return self._get_object(
            f'{self.url_base}/config/filterpolicy/versioninfo',
            '',
            'VersionInfo',
        )

    def get_guestLocations(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List guestLocation resources."""
        return self._get_objects(
            f'{self.url_base}/config/guestlocation',
            filter=filter,
            size=size,
            page=page,
        )

    def get_guestLocation_id(self, OID) -> dict:
        """Get a guestLocation resource by id."""
        return self._get_object(
            f'{self.url_base}/config/guestlocation',
            OID,
            'GuestLocation',
        )

    def get_guestLocation_versionInfo(self) -> dict:
        """Get guestLocation version information."""
        return self._get_object(
            f'{self.url_base}/config/guestlocation/versioninfo',
            '',
            'VersionInfo',
        )

    def get_guestSmtpNotificationSettings(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List guestSmtpNotificationSetting resources."""
        return self._get_objects(
            f'{self.url_base}/config/guestsmtpnotificationsettings',
            filter=filter,
            size=size,
            page=page,
        )

    def get_guestSmtpNotificationSetting_id(self, OID) -> dict:
        """Get a guestSmtpNotificationSetting resource by id."""
        return self._get_object(
            f'{self.url_base}/config/guestsmtpnotificationsettings',
            OID,
            'ERSGuestSmtpNotificationSettings',
        )

    def get_guestSmtpNotificationSetting_versionInfo(self) -> dict:
        """Get guestSmtpNotificationSetting version information."""
        return self._get_object(
            f'{self.url_base}/config/guestsmtpnotificationsettings/versioninfo',
            '',
            'VersionInfo',
        )

    def get_guestSsids(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List guestSsid resources."""
        return self._get_objects(
            f'{self.url_base}/config/guestssid',
            filter=filter,
            size=size,
            page=page,
        )

    def get_guestSsid_id(self, OID) -> dict:
        """Get a guestSsid resource by id."""
        return self._get_object(
            f'{self.url_base}/config/guestssid',
            OID,
            'GuestSsid',
        )

    def get_guestSsid_versionInfo(self) -> dict:
        """Get guestSsid version information."""
        return self._get_object(
            f'{self.url_base}/config/guestssid/versioninfo',
            '',
            'VersionInfo',
        )

    def get_guestTypes(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List guestType resources."""
        return self._get_objects(
            f'{self.url_base}/config/guesttype',
            filter=filter,
            size=size,
            page=page,
        )

    def get_guestType_id(self, OID) -> dict:
        """Get a guestType resource by id."""
        return self._get_object(
            f'{self.url_base}/config/guesttype',
            OID,
            'GuestType',
        )

    def get_guestType_versionInfo(self) -> dict:
        """Get guestType version information."""
        return self._get_object(
            f'{self.url_base}/config/guesttype/versioninfo',
            '',
            'VersionInfo',
        )

    def get_guestUsers(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List guestUser resources."""
        return self._get_objects(
            f'{self.url_base}/config/guestuser',
            filter=filter,
            size=size,
            page=page,
        )

    def get_guestUser_id(self, OID) -> dict:
        """Get a guestUser resource by id."""
        return self._get_object(
            f'{self.url_base}/config/guestuser',
            OID,
            'GuestUser',
        )

    def get_guestUser_name(self, name) -> dict:
        """Get a guestUser resource by name."""
        return self._get_object(
            f'{self.url_base}/config/guestuser/name',
            name,
            'GuestUser',
        )

    def get_guestUser_versionInfo(self) -> dict:
        """Get guestUser version information."""
        return self._get_object(
            f'{self.url_base}/config/guestuser/versioninfo',
            '',
            'VersionInfo',
        )

    def get_hotspotPortals(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List hotspotPortal resources."""
        return self._get_objects(
            f'{self.url_base}/config/hotspotportal',
            filter=filter,
            size=size,
            page=page,
        )

    def get_hotspotPortal_id(self, OID) -> dict:
        """Get a hotspotPortal resource by id."""
        return self._get_object(
            f'{self.url_base}/config/hotspotportal',
            OID,
            'HotspotPortal',
        )

    def get_hotspotPortal_versionInfo(self) -> dict:
        """Get hotspotPortal version information."""
        return self._get_object(
            f'{self.url_base}/config/hotspotportal/versioninfo',
            '',
            'VersionInfo',
        )

    def get_identity_groups(self, filter: str | list = None, size=20, page=1) -> dict:
        """List identityGroup resources."""
        return self._get_objects(
            f'{self.url_base}/config/identitygroup',
            filter=filter,
            size=size,
            page=page,
        )

    def get_identity_group_id(self, OID) -> dict:
        """Get a identityGroup resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/identitygroup',
            OID,
            'IdentityGroup',
        )

    def get_identity_group_name(self, name) -> dict:
        """Get a identityGroup resource by name."""
        return self._get_object(
            f'{self.url_base}/config/identitygroup/name',
            name,
            'IdentityGroup',
        )

    def get_identityGroup_versionInfo(self) -> dict:
        """Get identityGroup version information."""
        return self._get_object(
            f'{self.url_base}/config/identitygroup/versioninfo',
            '',
            'VersionInfo',
        )

    def get_idStoreSequences(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List idStoreSequence resources."""
        return self._get_objects(
            f'{self.url_base}/config/idstoresequence',
            filter=filter,
            size=size,
            page=page,
        )

    def get_idStoreSequence_id(self, OID) -> dict:
        """Get a idStoreSequence resource by id."""
        return self._get_object(
            f'{self.url_base}/config/idstoresequence',
            OID,
            'IdStoreSequence',
        )

    def get_idStoreSequence_name(self, name) -> dict:
        """Get a idStoreSequence resource by name."""
        return self._get_object(
            f'{self.url_base}/config/idstoresequence/name',
            name,
            'IdStoreSequence',
        )

    def get_idStoreSequence_versionInfo(self) -> dict:
        """Get idStoreSequence version information."""
        return self._get_object(
            f'{self.url_base}/config/idstoresequence/versioninfo',
            '',
            'VersionInfo',
        )

    def get_users(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List internalUser resources."""
        return self._get_objects(
            f'{self.url_base}/config/internaluser',
            filter=filter,
            size=size,
            page=page,
        )

    def get_user_id(self, OID) -> dict:
        """Get a internalUser resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/internaluser',
            OID,
            'InternalUser',
        )

    def get_user_name(self, name) -> dict:
        """Get a internalUser resource by name."""
        return self._get_object(
            f'{self.url_base}/config/internaluser/name',
            name,
            'InternalUser',
        )

    def get_internalUser_versionInfo(self) -> dict:
        """Get internalUser version information."""
        return self._get_object(
            f'{self.url_base}/config/internaluser/versioninfo',
            '',
            'VersionInfo',
        )

    def get_ldap_id(self, OID) -> dict:
        """Get a ldap resource by id."""
        return self._get_object(
            f'{self.url_base}/config/ldap',
            OID,
            'Ldap',
        )

    def get_ldap_name(self, name) -> dict:
        """Get a ldap resource by name."""
        return self._get_object(
            f'{self.url_base}/config/ldap/name',
            name,
            'Ldap',
        )

    def get_myDevicePortals(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List myDevicePortal resources."""
        return self._get_objects(
            f'{self.url_base}/config/mydeviceportal',
            filter=filter,
            size=size,
            page=page,
        )

    def get_myDevicePortal_id(self, OID) -> dict:
        """Get a myDevicePortal resource by id."""
        return self._get_object(
            f'{self.url_base}/config/mydeviceportal',
            OID,
            'MyDevicePortal',
        )

    def get_myDevicePortal_versionInfo(self) -> dict:
        """Get myDevicePortal version information."""
        return self._get_object(
            f'{self.url_base}/config/mydeviceportal/versioninfo',
            '',
            'VersionInfo',
        )

    def get_networkDevices(self, filter: str | list = None, size=20, page=1) -> dict:
        """List networkDevice resources."""
        return self._get_objects(
            f'{self.url_base}/config/networkdevice',
            filter=filter,
            size=size,
            page=page,
        )

    def get_networkDevice_id(self, OID) -> dict:
        """Get a networkDevice resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/networkdevice',
            OID,
            'NetworkDevice',
        )

    def get_networkDevice_name(self, name) -> dict:
        """Get a networkDevice resource by name."""
        return self._get_object(
            f'{self.url_base}/config/networkdevice/name',
            name,
            'NetworkDevice',
        )

    def get_networkDevice_versionInfo(self) -> dict:
        """Get networkDevice version information."""
        return self._get_object(
            f'{self.url_base}/config/networkdevice/versioninfo',
            '',
            'VersionInfo',
        )

    def get_networkDeviceGroups(self, filter: str | list = None, size=20, page=1) -> dict:
        """List networkDeviceGroup resources."""
        return self._get_objects(
            f'{self.url_base}/config/networkdevicegroup',
            filter=filter,
            size=size,
            page=page,
        )

    def get_networkDeviceGroup_id(self, OID) -> dict:
        """Get a networkDeviceGroup resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/networkdevicegroup',
            OID,
            'NetworkDeviceGroup',
        )

    def get_networkDeviceGroup_name(self, name) -> dict:
        """Get a networkDeviceGroup resource by name."""
        return self._get_object(
            f'{self.url_base}/config/networkdevicegroup/name',
            name,
            'NetworkDeviceGroup',
        )

    def get_networkDeviceGroup_versionInfo(self) -> dict:
        """Get networkDeviceGroup version information."""
        return self._get_object(
            f'{self.url_base}/config/networkdevicegroup/versioninfo',
            '',
            'VersionInfo',
        )

    def get_nspProfiles(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List nspProfile resources."""
        return self._get_objects(
            f'{self.url_base}/config/nspprofile',
            filter=filter,
            size=size,
            page=page,
        )

    def get_nspProfile_id(self, OID) -> dict:
        """Get a nspProfile resource by id."""
        return self._get_object(
            f'{self.url_base}/config/nspprofile',
            OID,
            'ERSNSPProfile',
        )

    def get_nspProfile_versionInfo(self) -> dict:
        """Get nspProfile version information."""
        return self._get_object(
            f'{self.url_base}/config/nspprofile/versioninfo',
            '',
            'VersionInfo',
        )

    def get_portals(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List portal resources."""
        return self._get_objects(
            f'{self.url_base}/config/portal',
            filter=filter,
            size=size,
            page=page,
        )

    def get_portal_id(self, OID) -> dict:
        """Get a portal resource by id."""
        return self._get_object(
            f'{self.url_base}/config/portal',
            OID,
            'ERSPortal',
        )

    def get_portal_versionInfo(self) -> dict:
        """Get portal version information."""
        return self._get_object(
            f'{self.url_base}/config/portal/versioninfo',
            '',
            'VersionInfo',
        )

    def get_portalGlobalSettings(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List portalGlobalSetting resources."""
        return self._get_objects(
            f'{self.url_base}/config/portalglobalsetting',
            filter=filter,
            size=size,
            page=page,
        )

    def get_portalGlobalSetting_id(self, OID) -> dict:
        """Get a portalGlobalSetting resource by id."""
        return self._get_object(
            f'{self.url_base}/config/portalglobalsetting',
            OID,
            'PortalCustomizationGlobalSetting',
        )

    def get_portalGlobalSetting_versionInfo(self) -> dict:
        """Get portalGlobalSetting version information."""
        return self._get_object(
            f'{self.url_base}/config/portalglobalsetting/versioninfo',
            '',
            'VersionInfo',
        )

    def get_portalThemes(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List portalTheme resources."""
        return self._get_objects(
            f'{self.url_base}/config/portaltheme',
            filter=filter,
            size=size,
            page=page,
        )

    def get_portalTheme_id(self, OID) -> dict:
        """Get a portalTheme resource by id."""
        return self._get_object(
            f'{self.url_base}/config/portaltheme',
            OID,
            'PortalTheme',
        )

    def get_portalTheme_versionInfo(self) -> dict:
        """Get portalTheme version information."""
        return self._get_object(
            f'{self.url_base}/config/portaltheme/versioninfo',
            '',
            'VersionInfo',
        )

    def get_profilerProfiles(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List profilerProfile resources."""
        return self._get_objects(
            f'{self.url_base}/config/profilerprofile',
            filter=filter,
            size=size,
            page=page,
        )

    def get_profilerProfile_id(self, OID) -> dict:
        """Get a profilerProfile resource by id."""
        return self._get_object(
            f'{self.url_base}/config/profilerprofile',
            OID,
            'ProfilerProfile',
        )

    def get_profilerProfile_versionInfo(self) -> dict:
        """Get profilerProfile version information."""
        return self._get_object(
            f'{self.url_base}/config/profilerprofile/versioninfo',
            '',
            'VersionInfo',
        )

    def get_pxGridSettings_versionInfo(self) -> dict:
        """Get pxGridSettings version information."""
        return self._get_object(
            f'{self.url_base}/config/pxgridsettings/versioninfo',
            '',
            'VersionInfo',
        )

    def get_radiusServerSequences(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List radiusServerSequence resources."""
        return self._get_objects(
            f'{self.url_base}/config/radiusserversequence',
            filter=filter,
            size=size,
            page=page,
        )

    def get_radiusServerSequence_id(self, OID) -> dict:
        """Get a radiusServerSequence resource by id."""
        return self._get_object(
            f'{self.url_base}/config/radiusserversequence',
            OID,
            'RadiusServerSequence',
        )

    def get_radiusServerSequence_versionInfo(self) -> dict:
        """Get radiusServerSequence version information."""
        return self._get_object(
            f'{self.url_base}/config/radiusserversequence/versioninfo',
            '',
            'VersionInfo',
        )

    def get_restIdStores(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List restIdStore resources."""
        return self._get_objects(
            f'{self.url_base}/config/restidstore',
            filter=filter,
            size=size,
            page=page,
        )

    def get_restIdStore_id(self, OID) -> dict:
        """Get a restIdStore resource by id."""
        return self._get_object(
            f'{self.url_base}/config/restidstore',
            OID,
            'RestIdStore',
        )

    def get_restIdStore_name(self, name) -> dict:
        """Get a restIdStore resource by name."""
        return self._get_object(
            f'{self.url_base}/config/restidstore/name',
            name,
            'RestIdStore',
        )

    def get_restIdStore_versionInfo(self) -> dict:
        """Get restIdStore version information."""
        return self._get_object(
            f'{self.url_base}/config/restidstore/versioninfo',
            '',
            'VersionInfo',
        )

    def get_selfRegPortals(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List selfRegPortal resources."""
        return self._get_objects(
            f'{self.url_base}/config/selfregportal',
            filter=filter,
            size=size,
            page=page,
        )

    def get_selfRegPortal_id(self, OID) -> dict:
        """Get a selfRegPortal resource by id."""
        return self._get_object(
            f'{self.url_base}/config/selfregportal',
            OID,
            'SelfRegPortal',
        )

    def get_selfRegPortal_versionInfo(self) -> dict:
        """Get selfRegPortal version information."""
        return self._get_object(
            f'{self.url_base}/config/selfregportal/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sgacls(self, filter: str | list = None, size=20, page=1) -> dict:
        """List sgacl resources."""
        return self._get_objects(
            f'{self.url_base}/config/sgacl',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sgacl_id(self, OID) -> dict:
        """Get a sgacl resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/sgacl',
            OID,
            'Sgacl',
        )

    def get_sgacl_versionInfo(self) -> dict:
        """Get sgacl version information."""
        return self._get_object(
            f'{self.url_base}/config/sgacl/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sgMappings(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sgMapping resources."""
        return self._get_objects(
            f'{self.url_base}/config/sgmapping',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sgMapping_id(self, OID) -> dict:
        """Get a sgMapping resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sgmapping',
            OID,
            'SgMapping',
        )

    def get_sgMapping_versionInfo(self) -> dict:
        """Get sgMapping version information."""
        return self._get_object(
            f'{self.url_base}/config/sgmapping/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sgMappingGroups(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sgMappingGroup resources."""
        return self._get_objects(
            f'{self.url_base}/config/sgmappinggroup',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sgMappingGroup_id(self, OID) -> dict:
        """Get a sgMappingGroup resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sgmappinggroup',
            OID,
            'SgMappingGroup',
        )

    def get_sgMappingGroup_versionInfo(self) -> dict:
        """Get sgMappingGroup version information."""
        return self._get_object(
            f'{self.url_base}/config/sgmappinggroup/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sgts(self, filter: str | list = None, size=20, page=1) -> dict:
        """List sgt resources."""
        return self._get_objects(
            f'{self.url_base}/config/sgt',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sgt_id(self, OID) -> dict:
        """Get a sgt resource by id."""
        if not self._oid_test(OID):
            from python_ise.python_ise import InvalidOID
            raise InvalidOID(
                f'{OID}. Must be in the form of 9h1713e4-jzeg-55ff-j59y-010y36061e95'
            )
        return self._get_object(
            f'{self.url_base}/config/sgt',
            OID,
            'Sgt',
        )

    def get_sgt_versionInfo(self) -> dict:
        """Get sgt version information."""
        return self._get_object(
            f'{self.url_base}/config/sgt/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sgtVnVlans(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sgtVnVlan resources."""
        return self._get_objects(
            f'{self.url_base}/config/sgtvnvlan',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sgtVnVlan_id(self, OID) -> dict:
        """Get a sgtVnVlan resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sgtvnvlan',
            OID,
            'SgtVnVlan',
        )

    def get_sgtVnVlan_versionInfo(self) -> dict:
        """Get sgtVnVlan version information."""
        return self._get_object(
            f'{self.url_base}/config/sgtvnvlan/versioninfo',
            '',
            'VersionInfo',
        )

    def get_smsProviders(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List smsProvider resources."""
        return self._get_objects(
            f'{self.url_base}/config/smsprovider',
            filter=filter,
            size=size,
            page=page,
        )

    def get_smsProvider_versionInfo(self) -> dict:
        """Get smsProvider version information."""
        return self._get_object(
            f'{self.url_base}/config/smsprovider/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sponsoredGuestPortals(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sponsoredGuestPortal resources."""
        return self._get_objects(
            f'{self.url_base}/config/sponsoredguestportal',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sponsoredGuestPortal_id(self, OID) -> dict:
        """Get a sponsoredGuestPortal resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sponsoredguestportal',
            OID,
            'SponsoredGuestPortal',
        )

    def get_sponsoredGuestPortal_versionInfo(self) -> dict:
        """Get sponsoredGuestPortal version information."""
        return self._get_object(
            f'{self.url_base}/config/sponsoredguestportal/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sponsorGroups(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sponsorGroup resources."""
        return self._get_objects(
            f'{self.url_base}/config/sponsorgroup',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sponsorGroup_id(self, OID) -> dict:
        """Get a sponsorGroup resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sponsorgroup',
            OID,
            'SponsorGroup',
        )

    def get_sponsorGroup_versionInfo(self) -> dict:
        """Get sponsorGroup version information."""
        return self._get_object(
            f'{self.url_base}/config/sponsorgroup/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sponsorGroupMembers(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sponsorGroupMember resources."""
        return self._get_objects(
            f'{self.url_base}/config/sponsorgroupmember',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sponsorGroupMember_versionInfo(self) -> dict:
        """Get sponsorGroupMember version information."""
        return self._get_object(
            f'{self.url_base}/config/sponsorgroupmember/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sponsorPortals(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sponsorPortal resources."""
        return self._get_objects(
            f'{self.url_base}/config/sponsorportal',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sponsorPortal_id(self, OID) -> dict:
        """Get a sponsorPortal resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sponsorportal',
            OID,
            'SponsorPortal',
        )

    def get_sponsorPortal_versionInfo(self) -> dict:
        """Get sponsorPortal version information."""
        return self._get_object(
            f'{self.url_base}/config/sponsorportal/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sxpLocalBindings(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sxpLocalBinding resources."""
        return self._get_objects(
            f'{self.url_base}/config/sxplocalbindings',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sxpLocalBinding_id(self, OID) -> dict:
        """Get a sxpLocalBinding resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sxplocalbindings',
            OID,
            'SxpLocalBinding',
        )

    def get_sxpLocalBinding_versionInfo(self) -> dict:
        """Get sxpLocalBinding version information."""
        return self._get_object(
            f'{self.url_base}/config/sxplocalbindings/versioninfo',
            '',
            'VersionInfo',
        )

    def get_systemCertificate_versionInfo(self) -> dict:
        """Get systemCertificate version information."""
        return self._get_object(
            f'{self.url_base}/config/systemcertificate/versioninfo',
            '',
            'VersionInfo',
        )

    def get_tacacsCommandSets(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List tacacsCommandSet resources."""
        return self._get_objects(
            f'{self.url_base}/config/tacacscommandsets',
            filter=filter,
            size=size,
            page=page,
        )

    def get_tacacsCommandSet_id(self, OID) -> dict:
        """Get a tacacsCommandSet resource by id."""
        return self._get_object(
            f'{self.url_base}/config/tacacscommandsets',
            OID,
            'TacacsCommandSets',
        )

    def get_tacacsCommandSet_name(self, name) -> dict:
        """Get a tacacsCommandSet resource by name."""
        return self._get_object(
            f'{self.url_base}/config/tacacscommandsets/name',
            name,
            'TacacsCommandSets',
        )

    def get_tacacsCommandSet_versionInfo(self) -> dict:
        """Get tacacsCommandSet version information."""
        return self._get_object(
            f'{self.url_base}/config/tacacscommandsets/versioninfo',
            '',
            'VersionInfo',
        )

    def get_tacacsExternalServers(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List tacacsExternalServer resources."""
        return self._get_objects(
            f'{self.url_base}/config/tacacsexternalservers',
            filter=filter,
            size=size,
            page=page,
        )

    def get_tacacsExternalServer_id(self, OID) -> dict:
        """Get a tacacsExternalServer resource by id."""
        return self._get_object(
            f'{self.url_base}/config/tacacsexternalservers',
            OID,
            'TacacsExternalServer',
        )

    def get_tacacsExternalServer_name(self, name) -> dict:
        """Get a tacacsExternalServer resource by name."""
        return self._get_object(
            f'{self.url_base}/config/tacacsexternalservers/name',
            name,
            'TacacsExternalServer',
        )

    def get_tacacsExternalServer_versionInfo(self) -> dict:
        """Get tacacsExternalServer version information."""
        return self._get_object(
            f'{self.url_base}/config/tacacsexternalservers/versioninfo',
            '',
            'VersionInfo',
        )

    def get_tacacsProfiles(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List tacacsProfile resources."""
        return self._get_objects(
            f'{self.url_base}/config/tacacsprofile',
            filter=filter,
            size=size,
            page=page,
        )

    def get_tacacsProfile_id(self, OID) -> dict:
        """Get a tacacsProfile resource by id."""
        return self._get_object(
            f'{self.url_base}/config/tacacsprofile',
            OID,
            'TacacsProfile',
        )

    def get_tacacsProfile_name(self, name) -> dict:
        """Get a tacacsProfile resource by name."""
        return self._get_object(
            f'{self.url_base}/config/tacacsprofile/name',
            name,
            'TacacsProfile',
        )

    def get_tacacsProfile_versionInfo(self) -> dict:
        """Get tacacsProfile version information."""
        return self._get_object(
            f'{self.url_base}/config/tacacsprofile/versioninfo',
            '',
            'VersionInfo',
        )

    def get_tacacsServerSequences(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List tacacsServerSequence resources."""
        return self._get_objects(
            f'{self.url_base}/config/tacacsserversequence',
            filter=filter,
            size=size,
            page=page,
        )

    def get_tacacsServerSequence_id(self, OID) -> dict:
        """Get a tacacsServerSequence resource by id."""
        return self._get_object(
            f'{self.url_base}/config/tacacsserversequence',
            OID,
            'TacacsServerSequence',
        )

    def get_tacacsServerSequence_name(self, name) -> dict:
        """Get a tacacsServerSequence resource by name."""
        return self._get_object(
            f'{self.url_base}/config/tacacsserversequence/name',
            name,
            'TacacsServerSequence',
        )

    def get_tacacsServerSequence_versionInfo(self) -> dict:
        """Get tacacsServerSequence version information."""
        return self._get_object(
            f'{self.url_base}/config/tacacsserversequence/versioninfo',
            '',
            'VersionInfo',
        )

    def get_ancPolicies(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List ancPolicy resources."""
        return self._get_objects(
            f'{self.url_base}/config/ancpolicy',
            filter=filter,
            size=size,
            page=page,
        )

    def get_ancPolicy_id(self, OID) -> dict:
        """Get a ancPolicy resource by id."""
        return self._get_object(
            f'{self.url_base}/config/ancpolicy',
            OID,
            'ANCPolicy',
        )

    def get_ancPolicy_name(self, name) -> dict:
        """Get a ancPolicy resource by name."""
        return self._get_object(
            f'{self.url_base}/config/ancpolicy/name',
            name,
            'ANCPolicy',
        )

    def get_ancPolicy_versionInfo(self) -> dict:
        """Get ancPolicy version information."""
        return self._get_object(
            f'{self.url_base}/config/ancpolicy/versioninfo',
            '',
            'VersionInfo',
        )

    def get_nodes(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List node resources."""
        return self._get_objects(
            f'{self.url_base}/config/node',
            filter=filter,
            size=size,
            page=page,
        )

    def get_node_id(self, OID) -> dict:
        """Get a node resource by id."""
        return self._get_object(
            f'{self.url_base}/config/node',
            OID,
            'Node',
        )

    def get_node_name(self, name) -> dict:
        """Get a node resource by name."""
        return self._get_object(
            f'{self.url_base}/config/node/name',
            name,
            'Node',
        )

    def get_node_versionInfo(self) -> dict:
        """Get node version information."""
        return self._get_object(
            f'{self.url_base}/config/node/versioninfo',
            '',
            'VersionInfo',
        )

    def get_sessionServiceNodes(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List sessionServiceNode resources."""
        return self._get_objects(
            f'{self.url_base}/config/sessionservicenode',
            filter=filter,
            size=size,
            page=page,
        )

    def get_sessionServiceNode_id(self, OID) -> dict:
        """Get a sessionServiceNode resource by id."""
        return self._get_object(
            f'{self.url_base}/config/sessionservicenode',
            OID,
            'SessionServiceNode',
        )

    def get_sessionServiceNode_name(self, name) -> dict:
        """Get a sessionServiceNode resource by name."""
        return self._get_object(
            f'{self.url_base}/config/sessionservicenode/name',
            name,
            'SessionServiceNode',
        )

    def get_sessionServiceNode_versionInfo(self) -> dict:
        """Get sessionServiceNode version information."""
        return self._get_object(
            f'{self.url_base}/config/sessionservicenode/versioninfo',
            '',
            'VersionInfo',
        )

    def get_pxGridNodes(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List pxGridNode resources."""
        return self._get_objects(
            f'{self.url_base}/config/pxgridnode',
            filter=filter,
            size=size,
            page=page,
        )

    def get_pxGridNode_id(self, OID) -> dict:
        """Get a pxGridNode resource by id."""
        return self._get_object(
            f'{self.url_base}/config/pxgridnode',
            OID,
            'PxgridNode',
        )

    def get_pxGridNode_name(self, name) -> dict:
        """Get a pxGridNode resource by name."""
        return self._get_object(
            f'{self.url_base}/config/pxgridnode/name',
            name,
            'PxgridNode',
        )

    def get_pxGridNode_versionInfo(self) -> dict:
        """Get pxGridNode version information."""
        return self._get_object(
            f'{self.url_base}/config/pxgridnode/versioninfo',
            '',
            'VersionInfo',
        )

    def get_ancEndpoints(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List ancEndpoint resources."""
        return self._get_objects(
            f'{self.url_base}/config/ancendpoint',
            filter=filter,
            size=size,
            page=page,
        )

    def get_ancEndpoint_id(self, OID) -> dict:
        """Get a ancEndpoint resource by id."""
        return self._get_object(
            f'{self.url_base}/config/ancendpoint',
            OID,
            'ANCEndPoint',
        )

    def get_ancEndpoint_versionInfo(self) -> dict:
        """Get ancEndpoint version information."""
        return self._get_object(
            f'{self.url_base}/config/ancendpoint/versioninfo',
            '',
            'VersionInfo',
        )

    def get_services(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List service resources."""
        return self._get_objects(
            f'{self.url_base}/config/service',
            filter=filter,
            size=size,
            page=page,
        )

    def get_service_id(self, OID) -> dict:
        """Get a service resource by id."""
        return self._get_object(
            f'{self.url_base}/config/service',
            OID,
            'ERSService',
        )

    def get_service_versionInfo(self) -> dict:
        """Get service version information."""
        return self._get_object(
            f'{self.url_base}/config/service/versioninfo',
            '',
            'VersionInfo',
        )

    def get_telemetryInfos(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List telemetryInfo resources."""
        return self._get_objects(
            f'{self.url_base}/config/telemetryinfo',
            filter=filter,
            size=size,
            page=page,
        )

    def get_telemetryInfo_id(self, OID) -> dict:
        """Get a telemetryInfo resource by id."""
        return self._get_object(
            f'{self.url_base}/config/telemetryinfo',
            OID,
            'TelemetryInfo',
        )

    def get_telemetryInfo_versionInfo(self) -> dict:
        """Get telemetryInfo version information."""
        return self._get_object(
            f'{self.url_base}/config/telemetryinfo/versioninfo',
            '',
            'VersionInfo',
        )

    def get_supportBundleStatuses(self, size=20, page=1, *, filter: str | list = None) -> dict:
        """List supportBundleStatus resources."""
        return self._get_objects(
            f'{self.url_base}/config/supportbundlestatus',
            filter=filter,
            size=size,
            page=page,
        )

    def get_supportBundleStatus_id(self, OID) -> dict:
        """Get a supportBundleStatus resource by id."""
        return self._get_object(
            f'{self.url_base}/config/supportbundlestatus',
            OID,
            'SBStatus',
        )

    def get_supportBundleStatus_versionInfo(self) -> dict:
        """Get supportBundleStatus version information."""
        return self._get_object(
            f'{self.url_base}/config/supportbundlestatus/versioninfo',
            '',
            'VersionInfo',
        )

    def get_threat_versionInfo(self) -> dict:
        """Get threat version information."""
        return self._get_object(
            f'{self.url_base}/config/threat/versioninfo',
            '',
            'VersionInfo',
        )

    def get_deploymentInfo_versionInfo(self) -> dict:
        """Get deploymentInfo version information."""
        return self._get_object(
            f'{self.url_base}/config/deploymentinfo/versioninfo',
            '',
            'VersionInfo',
        )

    def get_restIdStoreAttribute_versionInfo(self) -> dict:
        """Get restIdStoreAttribute version information."""
        return self._get_object(
            f'{self.url_base}/config/restidstoreattribute/versioninfo',
            '',
            'VersionInfo',
        )

    def get_restIdStoreSettings_versionInfo(self) -> dict:
        """Get restIdStoreSettings version information."""
        return self._get_object(
            f'{self.url_base}/config/restidstoresettings/versioninfo',
            '',
            'VersionInfo',
        )

    def get_supportBundleDownload_versionInfo(self) -> dict:
        """Get supportBundleDownload version information."""
        return self._get_object(
            f'{self.url_base}/config/supportbundledownload/versioninfo',
            '',
            'VersionInfo',
        )

    def get_supportBundle_versionInfo(self) -> dict:
        """Get supportBundle version information."""
        return self._get_object(
            f'{self.url_base}/config/supportbundle/versioninfo',
            '',
            'VersionInfo',
        )

