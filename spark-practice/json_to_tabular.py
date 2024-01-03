from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from pyspark.sql import DataFrame
from pyspark.sql.window import Window 

def main():
    spark = SparkSession.builder.getOrCreate()
    
    df = extract_data(spark)

    df_transformed = transform_data(df)
    df_transformed.show(1000000, truncate=False)

    load_data(df_transformed)

def extract_data(spark):
    df = (
        spark
        .read
        .option("multiLine",True)
        .json("data/")
    )

    return df

def transform_data(df):
    w = Window.orderBy("datetime")

    # Generar una columna con identificadores únicos
    df = df.withColumn("request_id", f.monotonically_increasing_id())

    # Desanidar la estructura "Journeys"
    df = df.withColumn("journey", f.explode(f.col("response.Journeys")))

    # Generar una columna con identificadores únicos para el nivel "journey"
    df = df.withColumn("journey_id", f.monotonically_increasing_id())

    # Desanidar la estructura "Portions"
    df = df.withColumn("portion", f.explode(f.col("journey.Portions")))

    # Generar una columna con identificadores únicos para el nivel "portion"
    df = df.withColumn("portion_id", f.monotonically_increasing_id())

    # Desanidar la estructura "Flights"
    df = df.withColumn("flight", f.explode(f.col("portion.Flights")))

    # Generar una columna con identificadores únicos para el nivel "flight"
    df = df.withColumn("flight_id", f.monotonically_increasing_id())

    # Desanidar la estructura "Availability"
    df = df.withColumn("availability", f.explode(f.col("flight.Availability")))

    # Realizar el cast del campo "State"
    df = df.withColumn("State", f.when(f.col("availability.State").rlike("^A\\d+$"), f.regexp_extract(f.col("availability.State"), r"^A(\d+)$", 1).cast("int")).otherwise(0))

    # Seleccionar las columnas requeridas y renombrarlas
    df = df.withColumn("DepartureAirport", f.col("request.Origin")) \
        .withColumn("ArrivalAirport", f.col("flight.ArrivalAirport")) \
        .withColumn("DepartureTime", f.col("flight.ArrivalTime")) \
        .select(
                "request_id",
                "datetime",
                "DepartureAirport",
                "journey_id",
                "ArrivalAirport",
                "DepartureTime",
                "portion_id",
                "availability.Cabin",
                "availability.RBD",
                "State",
                "flight_id"
            )
    
    return df

def load_data(df):
    (df
     .coalesce(1)
     .write
     .csv(f'final_data/result.csv', mode='overwrite', header=True)
    )

if __name__ == "__main__":
    main()

