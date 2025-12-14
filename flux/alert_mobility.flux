import "influxdata/influxdb/monitor"
import "influxdata/influxdb/v1"

data =
    from(bucket: "lunar-mission")
        |> range(start: -1m)
        |> filter(fn: (r) => r["_measurement"] == "comms" or r["_measurement"] == "mobility")
        |> filter(fn: (r) => r["_field"] == "battery_voltage")
        |> filter(fn: (r) => r["host"] == "lunar-gateway")
        |> filter(fn: (r) => r["unit"] == "rover-01")
        |> aggregateWindow(every: 1m, fn: last, createEmpty: false)

option task = {name: "Alert_mobility", every: 1m, offset: 0s}

check = {_check_id: "0ff347993a9c0000", _check_name: "Alert_mobility", _type: "threshold", tags: {}}
ok = (r) => r["battery_voltage"] > 20.0
crit = (r) => r["battery_voltage"] < 19.99
messageFn = (r) => "Check: ${ r._check_name } is: ${ r._level }"

data
    |> v1["fieldsAsCols"]()
    |> monitor["check"](data: check, messageFn: messageFn, ok: ok, crit: crit)
