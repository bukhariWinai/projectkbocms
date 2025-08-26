SELECT cmsapp_computeraccessory.deviceID,
cmsapp_computeraccessory.commodel,
cmsapp_computeraccessory.comspec,
cmsapp_repairstatus.status

FROM cmsapp_computeraccessory
INNER JOIN cmsapp_repairstatus
ON cmsapp_computeraccessory.comstatus_id = cmsapp_repairstatus.id
WHERE cmsapp_repairstatus.id = 4

