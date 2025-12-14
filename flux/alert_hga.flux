import "influxdata/influxdb/monitor"
import "influxdata/influxdb/v1"

data =
    from(bucket: "lunar-mission")
        |> range(start: -1m)
        |> filter(fn: (r) => r["_measurement"] == "comms")
        |> filter(fn: (r) => r["_field"] == "snr")
        |> aggregateWindow(every: 1m, fn: last, createEmpty: false)

option task = {name: "Alert_hga", every: 1m, offset: 0s}

check = {_check_id: "0ff347152f1c0000", _check_name: "Alert_hga", _type: "threshold", tags: {}}
ok = (r) => r["snr"] > 25.0
warn = (r) => r["snr"] < 24.99 and r["snr"] > 10.0
crit = (r) => r["snr"] < 9.99
messageFn = (r) => "Check: ${ r._check_name } is: ${ r._level }"

data
    |> v1["fieldsAsCols"]()
    |> monitor["check"](
        data: check,
        messageFn: messageFn,
        ok: ok,
        warn: warn,
        crit: crit,
    )
