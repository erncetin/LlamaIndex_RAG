from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from llama_index.embeddings.huggingface_api import HuggingFaceInferenceAPIEmbedding
from llama_index.core import Settings
from postgres_file import Postgres
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from llama_index.core import SQLDatabase
from sqlalchemy.sql import text
from llama_index.core.objects import SQLTableNodeMapping, ObjectIndex, SQLTableSchema
from llama_index.core.indices.struct_store.sql_query import SQLTableRetrieverQueryEngine
from llama_index.core import VectorStoreIndex


# Define the HuggingFace API token
HF_TOKEN = "<your_api_key>"

# Initialize a connection to the PostgreSQL database
connection = Postgres()
connection.clear_tables()  # Clear any existing tables
connection.create_tables()  # Create necessary tables
connection.insert_db()  # Insert initial data into the database

# Set up the SQLAlchemy engine and session for interacting with the PostgreSQL database
database_url = "postgresql://root:root@host_postgres:5432/db_postgres"
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Define the SQLDatabase object, specifying which tables to include
sql_database = SQLDatabase(engine, include_tables=["table1", "table2", "table3"])

# Set up the embedding model using the HuggingFace API
embedding_model = HuggingFaceInferenceAPIEmbedding(model_name="BAAI/bge-m3", token=HF_TOKEN)

# Set up the language model using the HuggingFace API
llm = HuggingFaceInferenceAPI(model_name="meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)

# Configure the settings to use the specified embedding model and language model
Settings.embed_model = embedding_model
Settings.llm = llm

# Define the mapping of SQL tables to node representations
table_node_mapping = SQLTableNodeMapping(sql_database)

# Define schemas for the SQL tables, providing context for each table
table_schema_objs = [
    SQLTableSchema(table_name="table1", context_str="This table has information of name, surname and date of birth informations of users"),
    SQLTableSchema(table_name="table2", context_str="This table has e-mail and date of birth information of users"),
    SQLTableSchema(table_name="table3", context_str="This table has name, age and date of birth information of users")
]

# Create an ObjectIndex from the table schemas and node mapping, using a vector store for indexing
obj_index = ObjectIndex.from_objects(
    table_schema_objs,
    table_node_mapping,
    VectorStoreIndex
)

# Initialize the query engine for retrieving data from the SQL tables
query_engine = SQLTableRetrieverQueryEngine(sql_database, obj_index.as_retriever())

# Define the query string to retrieve specific user information from the tables
query_str = "return the name, surname and date of birth of all users."

# Execute the query using the query engine
response = query_engine.query(query_str)

# Print the query response
print(response)
