import argparse
import logging
import psycopg2
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log",level=logging.DEBUG)

# postgresql database connectivity
logging.debug("Connecting to PostgreSQL...")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")

def put(name, snippet):
  """Store a snippet with an associated name. Returns the name and the snippet."""
  logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
  cursor = connection.cursor()
  command = "insert into snippets values (%s, %s)"
  cursor.execute(command, (name, snippet))
  connection.commit()
  logging.debug("Snippet stored successfully.")
  return name, snippet

def get(name):
  """Retrieve the snippet with a given name."""
  logging.info("Retrieving snippet {!r}".format(name))
  cursor = connection.cursor()
  command = "SELECT message FROM snippets WHERE keyword=%s"
  cursor.execute(command, (name,)) ### THAT'S going to take some getting used to...
  connection.commit()
  row = cursor.fetchone() # pull one row of results from db (only expect one row)
  return row[0]

def list():
  """
  Return a list of snippet names
  """
  logging.error("FIXME: Unimplemented - list()")
  pass # return names as list for display/printing?

def main():
  """Main function"""
  logging.info("Constructing parser...")
  parser = argparse.ArgumentParser(description="Store and retrieve snippets of text.")
  
  subparsers = parser.add_subparsers(dest="command", help="Available commands")
  
  # Subparser for "put" command
  logging.debug("Constructing <put> subparser...")
  put_parser = subparsers.add_parser("put", help="Store a snippet.")
  put_parser.add_argument("name", type=str,
                          help="Short name for snippet -- use double quotes to enclose spaces")
  put_parser.add_argument("snippet", type=str,
                          help="Snippet to store -- use double quotes to enclose spaces")
  
  # Subparser for "get" command
  logging.debug("Constructing <get> subparser...")
  get_parser = subparsers.add_parser("get", help="Retrieve a snippet.")
  get_parser.add_argument("name", type=str, 
                          help="Short name for snippet -- use double quotes to enclose spaces")
  
  arguments = parser.parse_args(sys.argv[1:])
  # Convert parsed arguments from namespace to dictionary
  arguments = vars(arguments)
  command = arguments.pop("command")
  
  if command == "put":
    name, snippet = put(**arguments)
    print("Stored {!r} as {!r}".format(snippet, name))
  elif command == "get":
    snippet = get(**arguments)
    print("Retrieved snippet: {!r}".format(snippet))

if __name__ == "__main__":
  main()
