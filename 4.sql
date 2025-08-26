SELECT cmsapp_profileuser.id ,cmsapp_repairandpartchange.deviceID,cmsapp_repairandpartchange.repaircase
FROM cmsapp_profileuser
INNER JOIN cmsapp_repairandpartchange
ON cmsapp_repairandpartchange.repairstatus_id = cmsapp_profileuser.id
WHERE owner_id = 131

