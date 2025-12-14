from(bucket: "lunar-mission")
  |> range(start: -1m)
  |> filter(fn: (r) => r["_measurement"] == "eclss")
  |> filter(fn: (r) => r["_field"] == "radiation" or r["_field"] == "pressure")
  |> last()
  |> map(fn: (r) => ({
      r with
      _level: 
        if r["_field"] == "radiation" and r["_value"] > 5.0 then "CRIT" 
        else if r["_field"] == "radiation" and r["_value"] > 2.0 then "WARN"
        else "OK"
    })
  )
  |> yield(name: "monitor_eclss")


# Nivel INFO no aparece
  # El enunciado pide niveles: OK, INFO, WARN, CRIT.
  # Aquí sólo tienes: "CRIT", "WARN", "OK".                   --> NO hace falta en nuestro contexto INFO porque no habría que enseñar --> es innecesario y suficiente con lo que ya tenemos
  # Te falta introducir algún caso donde devuelva "INFO"



  