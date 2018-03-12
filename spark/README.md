# setup

Spark cluster manager is buggy and seems to run as user that spins up the cluster.


	not sure yet

	brew install postgres

	./metatore_db.sh
	# see the conf/hive-site.xml especially the datanucleus.autoCreateSchema
	# see the packages jar settings for the driver
	# see the db commands on setup
	# all are apparently needed.

	In [1]: sc.getConf().getAll()
	Out[1]:
	[('spark.driver.host', '192.168.1.2'),
	 ('spark.driver.port', '60181'),
	 ('spark.jars',
	  'file:/Users/davidcottrell/.ivy2/jars/org.postgresql_postgresql-9.4.1207.jre7.jar'),
	 ('spark.app.id', 'local-1519771048910'),
	 ('spark.executor.id', 'driver'),
	 ('spark.app.name', 'PySparkShell'),
	 ('spark.driver.extraJavaOptions', '-Dderby.system.home=/tmp/derby'),
	 ('spark.sql.catalogImplementation', 'hive'),
	 ('spark.rdd.compress', 'True'),
	 ('spark.files',
	  'file:/Users/davidcottrell/.ivy2/jars/org.postgresql_postgresql-9.4.1207.jre7.jar'),
	 ('spark.submit.pyFiles',
	  '/Users/davidcottrell/.ivy2/jars/org.postgresql_postgresql-9.4.1207.jre7.jar'),
	 ('spark.serializer.objectStreamReset', '100'),
	 ('spark.master', 'local[*]'),
	 ('spark.submit.deployMode', 'client')]


https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html

Go straight to the examples.

	spark/examples/src/main/python
	spark/examples/src/main/python/sql/streaming/structured_network_wordcount.py
