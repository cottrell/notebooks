import contextlib

# use this as convenience, not suitable in general
_default_settings_for_local = [
    ("spark.sql.shuffle.partitions", "2")
    ]

def get_spark_conf(settings=None):
    from pyspark.conf import SparkConf
    conf = SparkConf()
    if settings is None:
        conf.setAll(_default_settings_for_local)
    else:
        conf.setAll(settings)
    return conf

def get_spark_context(conf):
    from pyspark import SparkContext
    # WARNING: not sure if this will not set conf if exist in all versions of spark
    sc = SparkContext.getOrCreate(conf=conf)
    return sc

def spark_context_is_stopped(sc):
    return sc._jsc.sc().isStopped()

def get_spark_session(conf):
    from pyspark.sql import SparkSession
    # WARNING: not sure if this will not set conf if exist in all versions of spark
    return SparkSession.builder.config(conf=conf).getOrCreate()

def get_spark_context_and_session(settings=None):
    conf = get_spark_conf(settings=settings)
    sc = get_spark_context(conf)
    spark = get_spark_session(conf)
    return sc, spark

@contextlib.contextmanager
def spark_manager(spark_master=None, name='default name'):
    if spark_master is None:
        spark_master = os.environ['SPARK_MASTER']
    conf = SparkConf().setMaster(spark_master) \
                      .setAppName(name) \
                      .set("spark.executor.memory", '1000m')
    spark_context = SparkContext(conf=conf)
    try:
        yield spark_context
    finally:
        spark_context.stop()

def reorder_schema(schema, names):
    schema_names = [x.name for x in schema]
    index = dict(zip(schema_names, range(len(schema_names))))
    new_schema = [schema[index[x]] for x in names]
    from pyspark.sql.types import StructType
    return StructType(new_schema)

def df_to_pasteable_spark_schema(df):
    return schema_tuples_to_pasteable_spark_schema(df_to_schema_tuples(df))

def df_to_spark_schema(df):
    return schema_tuples_to_spark_schema(df_to_schema_tuples(df))

def schema_tuples_to_pasteable_spark_schema(d, print_string=True):
    import pyspark.sql.types as t
    # convoluted but using actual objects as test
    s = list()
    for k, v in d:
        if v.startswith('int'):
            temp = k, t.IntegerType()
        elif v.startswith('object') or v.startswith('str'):
            temp = k, t.StringType()
        elif v.startswith('float'):
            temp = k, t.DoubleType()
        elif v.startswith('date'):
            temp = k, t.DateType()
        else:
            raise Exception('uh oh {} {}'.format(k, v))
        temp = 't.StructField("{}", t.{}())'.format(temp[0], temp[1])
        s.append(temp)
    s = '\n    ' + ',\n    '.join(s)
    s = "import pyspark.sql.types as t\nschema = t.StructType([{}\n    ])".format(s)
    if print_string:
        print(s)
    else:
        return s

def schema_tuples_to_spark_schema(d):
    import pyspark.sql.types as t
    s = list()
    for k, v in d:
        if v.startswith('int'):
            temp = k, t.IntegerType()
        elif v.startswith('object') or v.startswith('str'):
            temp = k, t.StringType()
        elif v.startswith('float'):
            temp = k, t.DoubleType()
        elif v.startswith('date'):
            temp = k, t.DateType()
        else:
            raise Exception('uh oh {} {}'.format(k, v))
        s.append(t.StructField(*temp))
    return t.StructType(s)

def dict_to_spark_schema(d):
    """ use tuples instead. spark schema are ordered so be careful """
    raise Exception('use schema_tuples_to_spark_schema')

