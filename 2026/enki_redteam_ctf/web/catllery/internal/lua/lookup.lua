local req_ticket_no = ARGV[1]
local holder_ticket_no = redis.call("HGET", KEYS[1], "holder_ticket_no")
if holder_ticket_no == false then
  return {}
end
if tonumber(req_ticket_no) ~= tonumber(holder_ticket_no) then
  return {}
end

local holder_name = redis.call("HGET", KEYS[1], "holder_name") or ""
local ttl = redis.call("TTL", KEYS[1])
if ttl < 0 then
  ttl = 0
end
return {ARGV[2], holder_ticket_no, holder_name, tostring(ttl)}
