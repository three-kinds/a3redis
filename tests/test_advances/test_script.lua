local function get_string_value(main_key)
    return redis.call("get", main_key)
end

local key_header = "test_"
local key_1 = ARGV[1]
local key_2 = ARGV[2]

return {
    tonumber(get_string_value(key_header..key_1)) - 10,
    tonumber(get_string_value(key_header..key_2)) - 10,
}
