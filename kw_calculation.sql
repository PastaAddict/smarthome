select device_id_ele,
case 
	when energi=0 then sum(opened_for)*kwh
	else sum(opened_for)*kwh + (julianday(CURRENT_TIMESTAMP) - julianday(max(opened_on)))* 24*kwh end total_consumption from
(select *,(julianday(closed_on) - julianday(opened_on))* 24  as opened_for  from
 (select command_id,command,date_time as opened_on,device_id_ele,
  lead (date_time) over(order by date_time) closed_on
  from
  (select command_id,command,date_time,device_id_ele from(select * from pragmatopoiei join elegxei on pragmatopoiei.command_id_pragma = elegxei.command_id_ele) e1
   join entoli on entoli.command_id = e1.command_id_ele
   where device_id_ele = '5fd688ab0cc1ed38ec8a7006' and (command = '5fe24dc2a42de2b58e74877f' or command = '5fe24e06a42de2b58e748780')))
 where command = '5fe24dc2a42de2b58e74877f') join syskeyi on device_id_ele = syskeyi.device_id
group by command