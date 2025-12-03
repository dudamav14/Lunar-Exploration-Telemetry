from(bucket: "lunar-mission")
  |> range(start: -1m)
  |> filter(fn: (r) => r["_measurement"] == "mobility")
  |> filter(fn: (r) => r["_field"] == "battery_voltage" or r["_field"] == "traction")
  |> last()
  |> map(fn: (r) => ({
      r with
      _level: 
        if r["_field"] == "battery_voltage" and r["_value"] < 20.0 then "CRIT"
        else if r["_field"] == "battery_voltage" and r["_value"] < 50.0 then "WARN"
        else if r["_field"] == "traction" and r["_value"] < 0.2 then "WARN"
        else "OK"
    })
  )
  |> yield(name: "monitor_mobility")