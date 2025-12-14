import "influxdata/influxdb/monitor"
import "influxdata/influxdb/v1"

data =
    from(bucket: "lunar-mission")
        |> range(start: -1m)
        |> filter(fn: (r) => r["_measurement"] == "eclss")
        |> filter(fn: (r) => r["_field"] == "radiation")
        |> filter(fn: (r) => r["host"] == "lunar-gateway")
        |> filter(fn: (r) => r["unit"] == "module-alpha")
        |> aggregateWindow(every: 1m, fn: last, createEmpty: false)

option task = {name: "Alert_eclss", every: 1m, offset: 0s}

check = {_check_id: "0ff34685fe1c0000", _check_name: "Alert_eclss", _type: "threshold", tags: {}}
crit = (r) => r["radiation"] > 5.0
ok = (r) => r["radiation"] < 0.3 and r["radiation"] > 0.06
warn = (r) => r["radiation"] < 4.99 and r["radiation"] > 0.31
messageFn = (r) => "Check: ${ r._check_name } is: ${ r._level }"

data
    |> v1["fieldsAsCols"]()
    |> monitor["check"](
        data: check,
        messageFn: messageFn,
        crit: crit,
        ok: ok,
        warn: warn,
    )
