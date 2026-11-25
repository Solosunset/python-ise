"""Generated compatibility registry. Do not edit; run python -m python_ise.generate."""

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

from types import MappingProxyType

# Legacy names keep their real hand-written ERS implementations; this registry
# records the names promised by the manifest so drift is testable.
LEGACY_NAMES: dict[str, tuple[str, ...]] = {
    'aciBindings': (
        'get_aciBindings',
    ),
    'aciSettings': (
        'get_aciSettings',
    ),
    'activeDirectory': (
    ),
    'adminuser': (
    ),
    'allowedProtocol': (
    ),
    'authorizationProfile': (
    ),
    'byodPortal': (
    ),
    'certificateProfile': (
    ),
    'certificateTemplate': (
    ),
    'downloadableACL': (
    ),
    'egressmatrixcell': (
        'get_egressmatrixcell',
        'get_egressMatrixCell_bulk',
        'add_egressmatrixcell',
        'update_egressmatrixcell',
        'delete_egressmatrixcell',
    ),
    'endpoint': (
        'get_endpoint_bulk',
        'get_endpoint_rejectedEndpoints',
        'get_endpoint_macAddress',
        'add_endpoint',
        'update_endpoint',
        'delete_endpoint',
        'get_all_endpoints',
        'async_get_all_endpoints',
    ),
    'endpointCert': (
    ),
    'endpointGroup': (
        'get_endpoint_groups',
        'get_endpoint_group',
        'get_all_endpoint_groups',
        'async_get_all_endpoint_groups',
    ),
    'externalRadiusServer': (
    ),
    'filterPolicy': (
    ),
    'guestLocation': (
    ),
    'guestSmtpNotificationSetting': (
    ),
    'guestSsid': (
    ),
    'guestType': (
    ),
    'guestUser': (
    ),
    'hotspotPortal': (
    ),
    'identityGroup': (
        'get_identityGroup_id',
        'get_identityGroup_name',
        'get_identityGroups',
    ),
    'idStoreSequence': (
    ),
    'internalUser': (
        'get_internalUser_id',
        'get_internalUser_name',
        'get_internalUsers',
        'add_user',
        'delete_user',
    ),
    'ldap': (
        'get_ldap',
        'get_ldap_hosts',
        'get_ldap_issuerCertificates',
        'get_ldap_rootCaCertificates',
    ),
    'myDevicePortal': (
    ),
    'networkDevice': (
        'get_networkDevice_bulk',
        'add_device',
        'delete_device',
    ),
    'networkDeviceGroup': (
    ),
    'nspProfile': (
    ),
    'portal': (
    ),
    'portalGlobalSetting': (
    ),
    'portalTheme': (
    ),
    'profilerProfile': (
    ),
    'pxGridSettings': (
    ),
    'radiusServerSequence': (
    ),
    'restIdStore': (
    ),
    'selfRegPortal': (
    ),
    'sgacl': (
        'get_sgacl_bulk',
        'get_sgacl_search',
        'add_sgacl',
        'update_sgacl',
        'delete_sgacl',
    ),
    'sgMapping': (
        'get_sgMapping_bulk',
    ),
    'sgMappingGroup': (
        'get_sgMappingGroup_bulk',
    ),
    'sgt': (
        'get_sgt_search',
        'add_sgt',
        'update_sgt',
        'delete_sgt',
    ),
    'sgtVnVlan': (
        'get_sgtVnVlan_bulk',
    ),
    'smsProvider': (
    ),
    'sponsoredGuestPortal': (
    ),
    'sponsorGroup': (
    ),
    'sponsorGroupMember': (
    ),
    'sponsorPortal': (
    ),
    'sxpConnection': (
        'get_sxpConnection_id',
        'get_sxpConnections',
        'get_sxpConnection_versionInfo',
        'get_sxpConnection_',
    ),
    'sxpLocalBinding': (
        'get_sxpLocalBinding_bulk',
    ),
    'sxpVpn': (
        'get_sxpVpn_id',
        'get_sxpVpns',
        'get_sxpVpn_versionInfo',
        'get_sxpVpn_bulk',
    ),
    'systemCertificate': (
    ),
    'tacacsCommandSet': (
    ),
    'tacacsExternalServer': (
    ),
    'tacacsProfile': (
    ),
    'tacacsServerSequence': (
    ),
    'ancPolicy': (
    ),
    'node': (
    ),
    'sessionServiceNode': (
    ),
    'pxGridNode': (
    ),
    'ancEndpoint': (
    ),
    'service': (
    ),
    'telemetryInfo': (
    ),
    'supportBundleStatus': (
    ),
    'threat': (
    ),
    'deploymentInfo': (
    ),
    'restIdStoreAttribute': (
    ),
    'restIdStoreSettings': (
    ),
    'supportBundleDownload': (
    ),
    'supportBundle': (
    ),
}

FACADE_SPECS: tuple[tuple[str, MappingProxyType], ...] = (
    ('acibindings', MappingProxyType({
        'version_info': 'get_acibinding_versionInfo',
    })),
    ('aci_settings', MappingProxyType({
        'version_info': 'get_aciSettings_versionInfo',
    })),
    ('active_directories', MappingProxyType({
        'list': 'get_activeDirectories',
        'by_id': 'get_activeDirectory_id',
        'by_name': 'get_activeDirectory_name',
        'version_info': 'get_activeDirectory_versionInfo',
    })),
    ('adminusers', MappingProxyType({
        'list': 'get_adminusers',
        'by_id': 'get_adminuser_id',
        'version_info': 'get_adminuser_versionInfo',
    })),
    ('allowed_protocols', MappingProxyType({
        'list': 'get_allowedProtocols',
        'by_id': 'get_allowedProtocol_id',
        'by_name': 'get_allowedProtocol_name',
        'version_info': 'get_allowedProtocol_versionInfo',
    })),
    ('authorization_profiles', MappingProxyType({
        'list': 'get_authorizationProfiles',
        'by_id': 'get_authorizationProfile_id',
        'by_name': 'get_authorizationProfile_name',
        'version_info': 'get_authorizationProfile_versionInfo',
    })),
    ('byod_portals', MappingProxyType({
        'list': 'get_byodPortals',
        'by_id': 'get_byodPortal_id',
        'version_info': 'get_byodPortal_versionInfo',
    })),
    ('certificate_profiles', MappingProxyType({
        'list': 'get_certificateProfiles',
        'by_id': 'get_certificateProfile_id',
        'version_info': 'get_certificateProfile_versionInfo',
    })),
    ('certificate_templates', MappingProxyType({
        'list': 'get_certificateTemplates',
        'by_id': 'get_certificateTemplate_id',
        'by_name': 'get_certificateTemplate_name',
        'version_info': 'get_certificateTemplate_versionInfo',
    })),
    ('downloadable_acls', MappingProxyType({
        'list': 'get_downloadableACLs',
        'by_id': 'get_downloadableACL_id',
        'version_info': 'get_downloadableACL_versionInfo',
    })),
    ('egressmatrixcells', MappingProxyType({
        'list': 'get_egressmatrixcells',
        'by_id': 'get_egressmatrixcell_id',
        'version_info': 'get_egressMatrixCell_versionInfo',
    })),
    ('endpoints', MappingProxyType({
        'list': 'get_endpoints',
        'by_id': 'get_endpoint_id',
        'by_name': 'get_endpoint_name',
        'version_info': 'get_endpoint_versionInfo',
    })),
    ('endpoint_certs', MappingProxyType({
        'version_info': 'get_endpointCert_versionInfo',
    })),
    ('endpoint_groups', MappingProxyType({
        'list': 'get_endpointGroups',
        'by_id': 'get_endpointGroup_id',
        'by_name': 'get_endpointGroup_name',
        'version_info': 'get_endpointGroup_versionInfo',
    })),
    ('external_radius_servers', MappingProxyType({
        'list': 'get_externalRadiusServers',
        'by_id': 'get_externalRadiusServer_id',
        'by_name': 'get_externalRadiusServer_name',
        'version_info': 'get_externalRadiusServer_versionInfo',
    })),
    ('filter_policies', MappingProxyType({
        'list': 'get_filterPolicies',
        'by_id': 'get_filterPolicy_id',
        'version_info': 'get_filterPolicy_versionInfo',
    })),
    ('guest_locations', MappingProxyType({
        'list': 'get_guestLocations',
        'by_id': 'get_guestLocation_id',
        'version_info': 'get_guestLocation_versionInfo',
    })),
    ('guest_smtp_notification_settings', MappingProxyType({
        'list': 'get_guestSmtpNotificationSettings',
        'by_id': 'get_guestSmtpNotificationSetting_id',
        'version_info': 'get_guestSmtpNotificationSetting_versionInfo',
    })),
    ('guest_ssids', MappingProxyType({
        'list': 'get_guestSsids',
        'by_id': 'get_guestSsid_id',
        'version_info': 'get_guestSsid_versionInfo',
    })),
    ('guest_types', MappingProxyType({
        'list': 'get_guestTypes',
        'by_id': 'get_guestType_id',
        'version_info': 'get_guestType_versionInfo',
    })),
    ('guest_users', MappingProxyType({
        'list': 'get_guestUsers',
        'by_id': 'get_guestUser_id',
        'by_name': 'get_guestUser_name',
        'version_info': 'get_guestUser_versionInfo',
    })),
    ('hotspot_portals', MappingProxyType({
        'list': 'get_hotspotPortals',
        'by_id': 'get_hotspotPortal_id',
        'version_info': 'get_hotspotPortal_versionInfo',
    })),
    ('identity_groups', MappingProxyType({
        'list': 'get_identity_groups',
        'by_id': 'get_identity_group_id',
        'by_name': 'get_identity_group_name',
        'version_info': 'get_identityGroup_versionInfo',
    })),
    ('id_store_sequences', MappingProxyType({
        'list': 'get_idStoreSequences',
        'by_id': 'get_idStoreSequence_id',
        'by_name': 'get_idStoreSequence_name',
        'version_info': 'get_idStoreSequence_versionInfo',
    })),
    ('internal_users', MappingProxyType({
        'list': 'get_users',
        'by_id': 'get_user_id',
        'by_name': 'get_user_name',
        'version_info': 'get_internalUser_versionInfo',
    })),
    ('ldaps', MappingProxyType({
        'by_id': 'get_ldap_id',
        'by_name': 'get_ldap_name',
    })),
    ('my_device_portals', MappingProxyType({
        'list': 'get_myDevicePortals',
        'by_id': 'get_myDevicePortal_id',
        'version_info': 'get_myDevicePortal_versionInfo',
    })),
    ('network_devices', MappingProxyType({
        'list': 'get_networkDevices',
        'by_id': 'get_networkDevice_id',
        'by_name': 'get_networkDevice_name',
        'version_info': 'get_networkDevice_versionInfo',
    })),
    ('network_device_groups', MappingProxyType({
        'list': 'get_networkDeviceGroups',
        'by_id': 'get_networkDeviceGroup_id',
        'by_name': 'get_networkDeviceGroup_name',
        'version_info': 'get_networkDeviceGroup_versionInfo',
    })),
    ('nsp_profiles', MappingProxyType({
        'list': 'get_nspProfiles',
        'by_id': 'get_nspProfile_id',
        'version_info': 'get_nspProfile_versionInfo',
    })),
    ('portals', MappingProxyType({
        'list': 'get_portals',
        'by_id': 'get_portal_id',
        'version_info': 'get_portal_versionInfo',
    })),
    ('portal_global_settings', MappingProxyType({
        'list': 'get_portalGlobalSettings',
        'by_id': 'get_portalGlobalSetting_id',
        'version_info': 'get_portalGlobalSetting_versionInfo',
    })),
    ('portal_themes', MappingProxyType({
        'list': 'get_portalThemes',
        'by_id': 'get_portalTheme_id',
        'version_info': 'get_portalTheme_versionInfo',
    })),
    ('profiler_profiles', MappingProxyType({
        'list': 'get_profilerProfiles',
        'by_id': 'get_profilerProfile_id',
        'version_info': 'get_profilerProfile_versionInfo',
    })),
    ('pxgrid_settings', MappingProxyType({
        'version_info': 'get_pxGridSettings_versionInfo',
    })),
    ('radius_server_sequences', MappingProxyType({
        'list': 'get_radiusServerSequences',
        'by_id': 'get_radiusServerSequence_id',
        'version_info': 'get_radiusServerSequence_versionInfo',
    })),
    ('rest_id_stores', MappingProxyType({
        'list': 'get_restIdStores',
        'by_id': 'get_restIdStore_id',
        'by_name': 'get_restIdStore_name',
        'version_info': 'get_restIdStore_versionInfo',
    })),
    ('self_reg_portals', MappingProxyType({
        'list': 'get_selfRegPortals',
        'by_id': 'get_selfRegPortal_id',
        'version_info': 'get_selfRegPortal_versionInfo',
    })),
    ('sgacls', MappingProxyType({
        'list': 'get_sgacls',
        'by_id': 'get_sgacl_id',
        'version_info': 'get_sgacl_versionInfo',
    })),
    ('sg_mappings', MappingProxyType({
        'list': 'get_sgMappings',
        'by_id': 'get_sgMapping_id',
        'version_info': 'get_sgMapping_versionInfo',
    })),
    ('sg_mapping_groups', MappingProxyType({
        'list': 'get_sgMappingGroups',
        'by_id': 'get_sgMappingGroup_id',
        'version_info': 'get_sgMappingGroup_versionInfo',
    })),
    ('sgts', MappingProxyType({
        'list': 'get_sgts',
        'by_id': 'get_sgt_id',
        'version_info': 'get_sgt_versionInfo',
    })),
    ('sgt_vn_vlans', MappingProxyType({
        'list': 'get_sgtVnVlans',
        'by_id': 'get_sgtVnVlan_id',
        'version_info': 'get_sgtVnVlan_versionInfo',
    })),
    ('sms_providers', MappingProxyType({
        'list': 'get_smsProviders',
        'version_info': 'get_smsProvider_versionInfo',
    })),
    ('sponsored_guest_portals', MappingProxyType({
        'list': 'get_sponsoredGuestPortals',
        'by_id': 'get_sponsoredGuestPortal_id',
        'version_info': 'get_sponsoredGuestPortal_versionInfo',
    })),
    ('sponsor_groups', MappingProxyType({
        'list': 'get_sponsorGroups',
        'by_id': 'get_sponsorGroup_id',
        'version_info': 'get_sponsorGroup_versionInfo',
    })),
    ('sponsor_group_members', MappingProxyType({
        'list': 'get_sponsorGroupMembers',
        'version_info': 'get_sponsorGroupMember_versionInfo',
    })),
    ('sponsor_portals', MappingProxyType({
        'list': 'get_sponsorPortals',
        'by_id': 'get_sponsorPortal_id',
        'version_info': 'get_sponsorPortal_versionInfo',
    })),
    ('sxp_connections', MappingProxyType({
    })),
    ('sxp_local_bindings', MappingProxyType({
        'list': 'get_sxpLocalBindings',
        'by_id': 'get_sxpLocalBinding_id',
        'version_info': 'get_sxpLocalBinding_versionInfo',
    })),
    ('sxp_vpns', MappingProxyType({
    })),
    ('system_certificates', MappingProxyType({
        'version_info': 'get_systemCertificate_versionInfo',
    })),
    ('tacacs_command_sets', MappingProxyType({
        'list': 'get_tacacsCommandSets',
        'by_id': 'get_tacacsCommandSet_id',
        'by_name': 'get_tacacsCommandSet_name',
        'version_info': 'get_tacacsCommandSet_versionInfo',
    })),
    ('tacacs_external_servers', MappingProxyType({
        'list': 'get_tacacsExternalServers',
        'by_id': 'get_tacacsExternalServer_id',
        'by_name': 'get_tacacsExternalServer_name',
        'version_info': 'get_tacacsExternalServer_versionInfo',
    })),
    ('tacacs_profiles', MappingProxyType({
        'list': 'get_tacacsProfiles',
        'by_id': 'get_tacacsProfile_id',
        'by_name': 'get_tacacsProfile_name',
        'version_info': 'get_tacacsProfile_versionInfo',
    })),
    ('tacacs_server_sequences', MappingProxyType({
        'list': 'get_tacacsServerSequences',
        'by_id': 'get_tacacsServerSequence_id',
        'by_name': 'get_tacacsServerSequence_name',
        'version_info': 'get_tacacsServerSequence_versionInfo',
    })),
    ('anc_policies', MappingProxyType({
        'list': 'get_ancPolicies',
        'by_id': 'get_ancPolicy_id',
        'by_name': 'get_ancPolicy_name',
        'version_info': 'get_ancPolicy_versionInfo',
    })),
    ('nodes', MappingProxyType({
        'list': 'get_nodes',
        'by_id': 'get_node_id',
        'by_name': 'get_node_name',
        'version_info': 'get_node_versionInfo',
    })),
    ('session_service_nodes', MappingProxyType({
        'list': 'get_sessionServiceNodes',
        'by_id': 'get_sessionServiceNode_id',
        'by_name': 'get_sessionServiceNode_name',
        'version_info': 'get_sessionServiceNode_versionInfo',
    })),
    ('pxgrid_nodes', MappingProxyType({
        'list': 'get_pxGridNodes',
        'by_id': 'get_pxGridNode_id',
        'by_name': 'get_pxGridNode_name',
        'version_info': 'get_pxGridNode_versionInfo',
    })),
    ('anc_endpoints', MappingProxyType({
        'list': 'get_ancEndpoints',
        'by_id': 'get_ancEndpoint_id',
        'version_info': 'get_ancEndpoint_versionInfo',
    })),
    ('services', MappingProxyType({
        'list': 'get_services',
        'by_id': 'get_service_id',
        'version_info': 'get_service_versionInfo',
    })),
    ('telemetry_infos', MappingProxyType({
        'list': 'get_telemetryInfos',
        'by_id': 'get_telemetryInfo_id',
        'version_info': 'get_telemetryInfo_versionInfo',
    })),
    ('support_bundle_statuses', MappingProxyType({
        'list': 'get_supportBundleStatuses',
        'by_id': 'get_supportBundleStatus_id',
        'version_info': 'get_supportBundleStatus_versionInfo',
    })),
    ('threats', MappingProxyType({
        'version_info': 'get_threat_versionInfo',
    })),
    ('deployment_infos', MappingProxyType({
        'version_info': 'get_deploymentInfo_versionInfo',
    })),
    ('rest_id_store_attributes', MappingProxyType({
        'version_info': 'get_restIdStoreAttribute_versionInfo',
    })),
    ('rest_id_store_settings', MappingProxyType({
        'version_info': 'get_restIdStoreSettings_versionInfo',
    })),
    ('support_bundle_downloads', MappingProxyType({
        'version_info': 'get_supportBundleDownload_versionInfo',
    })),
    ('support_bundles', MappingProxyType({
        'version_info': 'get_supportBundle_versionInfo',
    })),
)
