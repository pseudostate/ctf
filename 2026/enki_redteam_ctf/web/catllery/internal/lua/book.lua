if redis.call("EXISTS", KEYS[1]) == 1 then
  return "seat_taken"
end
if redis.call("EXISTS", KEYS[2]) == 1 then
  return "already_holding_seat"
end
redis.call("HSET", KEYS[1], "holder_ticket_no", ARGV[2], "holder_name", ARGV[3])
redis.call("EXPIRE", KEYS[1], ARGV[4])
redis.call("SET", KEYS[2], ARGV[1], "EX", ARGV[4])
return "ok"
