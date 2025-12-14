from(bucket: "lunar-mission")
  |> range(start: -1m)
  |> filter(fn: (r) => r["_measurement"] == "comms")
  |> filter(fn: (r) => r["_field"] == "ber" or r["_field"] == "latency")
  |> last()
  |> map(fn: (r) => ({
      r with
      _level: 
        if r["_field"] == "ber" and r["_value"] > 0.01 then "CRIT"
        else if r["_field"] == "latency" and r["_value"] > 500.0 then "WARN"
        else "OK"
    })
  )
  |> yield(name: "monitor_hga")

 