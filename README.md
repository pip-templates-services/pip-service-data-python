# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Sample data microservice

This is a sample data microservice that stores and retries generic entities. This microservice shall be used
as a template to create general purpose data microservices.

Supported functionality:
* Deployment platforms: Standalone Process, Docker, AWS Lambda
* External APIs: HTTP (REST and Commandable), GRPC (Custom and Commandable)
* Persistence: Memory, Flat Files, MongoDB, PosgreSQL (Relational and NoSQL), SQLServer (Relational and NoSQL), MySql (Relational and NoSQL)
* Health checks: Heartbeat, Status
* Consolidated logging: ElasticSearch, CloudWatch
* Consolidated metrics: Prometheus, CloudWatch

This microservice does not depend on other microservices.

Key patterns implemented in this library:

**Zero-time onboarding:** A new developer doesn't have to have a prior khowledge of the code
nor preinstalled and preconfigured development environment.
To get started with any component he/she just need to do 3 simple steps:
+ Checkout the code
+ Launch dependencies via [docker-compose.dev.yml](docker/docker-compose.dev.yml)
+ Execute **npm test** or **npm run**. 

**Automated build and test processes:** Clear, build and test actions are dockerized and scripted.
The scripts shall be run before committing the code. And the same scripts shall be executed in automated
CI/CD pipelines. That approach allows to make identical build and test actions across the entire delivery
pipeline. And have a clear separation between developer and DevOps roles (developers are responsible
for individual components, their build, test and packaging. DevOps are responsible for running CI/CD pipelines, assembling and testing entire system from individual components).

**Multiple persistence options:** This microservice contains persistence for several databases. During the deployment time, based on configuration settings a particular type of persistence can be activated and included into the microservice configuration. That entire process can be done without any code changes.

**Multiple communication protocols:** The microservice contains services that allow to connect several different ways, depending on the environment or client requirements. For instance: on-premises the microservice can be deployed as a docker container. Locally it can be called via GRPC interface and externally via REST. When the same microservice is deployed on AWS cloud as a Lambda function, it can be called using the LambdaClient. Moreover, several microservice can be packaged into a single process, essentially represending a monolith. In that scenario, then can be called using in-process calls using the DirectClient.

**Monitoring and Observability:** All services are instrumented to collect logs of called operations, metrics that collect number of calls, average call times and number of erors, and traces. Depending on the deployment configuration that information can be sent to different destinations: console, Promethous, ApplicationInsights, CloudWatch and others. Additionally, the microservice exposes additional heartbeat and status endpoints that can be used for health monitoring.

**Versioning:** Data objects and clients are versioned from the beginning. When breaking changes are introduced into the microservice, it shall keep the old version of the interface for backward-compatibility and expose a new version of the interface simultaniously. Then client library will have a new set of objects and clients for the new version, while keeping the old one intact. That will provide a clear versioning and backward-compatibility for users of the microservice.

<a name="links"></a> Quick links:

* Communication Protocols:
  - [gRPC Version 1](pip_service_data_python/protos/entities_v1.proto)
  - [HTTP Version 1](pip_service_data_python/swagger/entities_v1.yaml)
* Client SDKs:
  - [Node.js SDK](https://github.com/pip-templates-services/pip-client-data-nodex)
  - [.NET SDK](https://github.com/pip-templates-services/pip-client-data-dotnet)
  - [Golang SDK](https://github.com/pip-templates-services/pip-client-data-go)
* [API Reference](https://pip-templates-services.github.io/pip-service-data-python/index.html)
* [Change Log](CHANGELOG.md)
* [Packing pyodbc driver for SQLServer on AWS Lambda](https://medium.com/@narayan.anurag/breaking-the-ice-between-aws-lambda-pyodbc-6f53d5e2bd26)


## Contract

The contract of the microservice is presented below. 

```python

class EntityV1(IStringIdentifiable):
    def __init__(self, id: str = None, site_id: str = None, type: str = None, name: str = None, content: str = None):
        self.id = id            # Entity ID
        self.type = type        # ID of a work site (field installation)
        self.site_id = site_id  # Entity type: Type2, Type1 or Type3
        self.name = name        # Human readable name
        self.content = content  # String content

class IEntitiesClientV1(ABC):

    def get_entities(self, correlation_id: Optional[str], filter_params: FilterParams, paging: PagingParams) -> DataPage:
        raise NotImplementedError("Method is not implemented")

    def get_entities_by_id(self, correlation_id: Optional[str], entity_id: str) -> EntityV1:
        raise NotImplementedError("Method is not implemented")

    def get_entity_by_name(self, correlation_id: Optional[str], entity_name: str) -> EntityV1:
        raise NotImplementedError("Method is not implemented")

    def create_entity(self, correlation_id: Optional[str], entity: EntityV1) -> EntityV1:
        raise NotImplementedError("Method is not implemented")

    def update_entity(self, correlation_id: Optional[str], entity: EntityV1) -> EntityV1:
        raise NotImplementedError("Method is not implemented")

    def delete_entity_by_id(self, correlation_id: Optional[str], entity_id: str) -> EntityV1:
        raise NotImplementedError("Method is not implemented")


```

## Get

Get the microservice source from GitHub:
```bash
git clone git@github.com:pip-templates-services/pip-service-data-python.git
```

Install the microservice dependencies:
```bash
pip install -r requirements.txt
```

Get docker image for the microservice:
```bash
docker pull pipdevs/pip-service-data-python:latest
```
## Run

The microservice can be configured using the environment variables:
* AWS_LAMDBA_ARN - a unique Amazon Resource Name
* AWS_ACCESS_ID - AWS access/client id
* AWS_ACCESS_KEY - AWS access/client id
* CLOUD_WATCH_ENABLED -  turn on CloudWatch loggers and metrics
* CLOUD_WATCH_STREAM - Cloud Watch Log stream (default: context name)
* CLOUD_WATCH_GROUP - Cloud Watch Log group (default: context instance ID or hostname)
* ELASTICSEARCH_LOGGING_ENABLED - turn on Elasticsearch logs and metrics
* ELASTICSEARCH_PROTOCOL - connection protocol: http or https
* ELASTICSEARCH_SERVICE_URI - resource URI or connection string with all parameters in it
* ELASTICSEARCH_SERVICE_HOST - host name or IP address
* ELASTICSEARCH_SERVICE_PORT - port number
* FILE_ENABLED - turn on file persistence. Keep it undefined to turn it off
* FILE_PATH - file path where persistent data shall be stored (default: ../data/id_records.json) 
* MEMORY_ENABLED - turn on in-memory persistence. Keep it undefined to turn it off
* MONGO_ENABLED - turn on MongoDB persistence. Keep it undefined to turn it off
* MONGO_SERVICE_URI - URI to connect to MongoDB. When it's defined other database parameters are ignored
* MONGO_SERVICE_HOST - MongoDB hostname or server address
* MONGO_SERVICE_PORT - MongoDB port number (default: 3360)
* MONGO_DB - MongoDB database name (default: app)
* MONGO_COLLECTION - MongoDB collection (default: id_records)
* MONGO_USER - MongoDB user login
* MONGO_PASS - MongoDB user password
* MYSQL_ENABLED - turn on MySql persistence. Keep it undefined to turn it off
* MYSQL_JSON_ENABLED - turn on JSON MySql persistence. Keep it undefined to turn it off
* MYSQL_URI - URI to connect to MySql. When it's defined other database parameters are ignored
* MYSQL_HOST - MySql hostname or server address
* MYSQL_PORT - MySql port number (default: 3306)
* MYSQL_DB - MySql database name (default: test)
* MYSQL_USER - MySql user login
* MYSQL_PASSWORD - MySql user password
* POSTGRES_ENABLED - turn on PostgreSQL persistence. Keep it undefined to turn it off
* POSTGRES_JSON_ENABLED - turn on JSON PostgreSQL persistence. Keep it undefined to turn it off
* POSTGRES_SERVICE_URI - URI to connect to PostgreSQL. When it's defined other database parameters are ignored
* POSTGRES_SERVICE_HOST - PostgreSQL hostname or server address
* POSTGRES_SERVICE_PORT - PostgreSQL port number (default: 5432)
* POSTGRES_DB - PostgreSQL database name (default: app)
* POSTGRES_TABLE - PostgreSQL table (default: id_records)
* POSTGRES_USER - PostgreSQL user login
* POSTGRES_PASS - PostgreSQL user password
* PUSHGATEWAY_METRICS_ENABLED - turn on pushgetway for prometheus
* PUSHGATEWAY_PROTOCOL - connection protocol: http or https
* PUSHGATEWAY_METRICS_SERVICE_URI - resource URI or connection string with all parameters in it
* PUSHGATEWAY_METRICS_SERVICE_HOST - host name or IP address
* PUSHGATEWAY_METRICS_SERVICE_PORT - port number
* SQLSERVER_ENABLED - turn on SQL Server persistence. Keep it undefined to turn it off
* SQLSERVER_JSON_ENABLED - turn on JSON SQL Server persistence. Keep it undefined to turn it off
* SQLSERVER_SERVICE_URI - URI to connect to SQL Server. When it's defined other database parameters are ignored
* SQLSERVER_SERVICE_HOST - SQL Server hostname or server address
* SQLSERVER_SERVICE_PORT - SQL Server port number (default: 1433)
* SQLSERVER_DB - SQL Server database name (default: app)
* SQLSERVER_TABLE - SQL Server table (default: id_records)
* SQLSERVER_USER - SQL Server user login
* SQLSERVER_PASS - SQL Server user password
* HTTP_ENABLED - turn on HTTP endpoint
* HTTP_PORT - HTTP port number (default: 8080)
* GRPC_ENABLED - turn on GRPC endpoint
* GRPC_PORT - GRPC port number (default: 8090)


Start the microservice as process:
```bash
python ./bin/main.py
```

Run the microservice in docker:
Then use the following command:
```bash
./run.ps1
```

Launch the microservice with all infrastructure services using docker-compose:
```bash
docker-compose -f ./docker/docker-compose.yml up
```

## Use

Install the client pip package as
```bash
pip install pip-client-data-python
```

Inside your code get the reference to the client SDK
```python
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import FilterParams, PagingParams

from pip_service_data_python.data.EntityTypeV1 import EntityTypeV1
from pip_service_data_python.data.EntityV1 import EntityV1

from pip_client_data_python.clients.version1 import EntitiesCommandableHttpClientV1
```

Instantiate the client
```python
# Create the client instance
client = EntitiesCommandableHttpClientV1()
```

Define client connection parameters
```python
# Client configuration
http_config = ConfigParams.from_tuples(
	"connection.protocol", "http",
	"connection.host", "localhost",
	"connection.port", 8080
)
# Configure the client
client.configure(http_config)
```

Connect to the microservice
```python
# Connect to the microservice
client.open(None)
    
# Work with the microservice
...
```

Call the microservice using the client API
```python
# Define a entity
entity = EntityV1(
    id= '1',
    site_id= '1',
    type= EntityTypeV1.Type1,
    name= '00001',
    content= 'ABC'
)

# Create the entity
entity = self.client.create_entity(None, ENTITY1)

# Do something with the returned entity...

# Get a list of entities
page = self.client.get_entities(
    None,
    FilterParams.from_tuples(
        "name", "TestEntity",
    ),
    PagingParams(0, 10)
)

# Do something with the returned page...
# E.g. entity = page['data'][0]
```

## Develop

For development you shall install the following prerequisites:
* Python 3.6+
* Visual Studio Code or another IDE of your choice
* Docker

Install dependencies:
```bash
pip install -r requirements.txt
```

Before running tests launch infrastructure services and required microservices:
```bash
docker-compose -f ./docker-compose.dev.yml up
```

Run automated tests:
```bash
pytest
```

Generate GRPC protobuf stubs:
```bash
./protogen.ps1
```

Generate API documentation:
```bash
./docgen.ps1
```

Before committing changes run dockerized build and test as:
```bash
./build.ps1
./test.ps1
./package.ps1
./run.ps1
./clear.ps1
```

## Contacts

This microservice was created and currently maintained by *Sergey Seroukhov* and *Danil Prisyzhniy*.
