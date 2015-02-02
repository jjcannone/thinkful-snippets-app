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

def put(name, snippet, hide, show):
  """Store a snippet with an associated name. Returns the name and the snippet."""
  logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
  truth = "true" if hide else "false"
  with connection, connection.cursor() as cursor:
    try:
      cursor.execute("INSERT INTO snippets VALUES (%s, %s, %s)", (name, snippet, truth))
      logging.debug("Snippet stored successfully.")
      print("Stored snippet {!r} under name {!r}".format(snippet, name))
    except psycopg2.IntegrityError as e:
      connection.rollback()
      cursor.execute("UPDATE snippets SET message=%s, hidden=%s WHERE keyword=%s", 
                     (snippet, truth, name))
      logging.debug("Snippet updated successfully.")
      print("Updated name {!r} as snippet {!r}".format(name, snippet))
  return name, snippet

def get(name):
  """Retrieve the snippet with a given name."""
  logging.info("Retrieving snippet {!r}".format(name))
#  cursor = connection.cursor()
#  cursor.execute(command, (name,)) ### THAT'S going to take some getting used to...
#  row = cursor.fetchone() # pull one row of results from db (only expect one row due to PK)
#  connection.commit()
  with connection, connection.cursor() as cursor:
    cursor.execute("SELECT message FROM snippets WHERE keyword=%s AND hidden=f", (name,))
    row = cursor.fetchone()

  if row:
    print("Retrieved snippet: {!r}".format(name))
    return row[0]
  else:
    logging.debug("Requested snippet name ({!r}) was not found in the database.".format(name))

def list():
  """Return a list of snippet names"""
  logging.info("List snippets from database")
  print("Name: Snippet")
  with connection, connection.cursor() as cursor:
    cursor.execute("SELECT keyword, message FROM snippets WHERE hidden='f' ORDER BY keyword")
    for row in cursor.fetchall():
      print ("{!r}: {!r}".format(row[0],row[1]))

def search(search_string):
  """Return a list of snippet names that match the input string"""
  logging.info("Search for input string in snippets")
  print("Name: Snippet")
  with connection, connection.cursor() as cursor:
    cursor.execute("SELECT keyword, message FROM snippets WHERE message LIKE %s AND hidden='f' ORDER BY keyword",
                  ("%"+search_string+"%",))
    for row in cursor.fetchall():
      print ("{!r}: {!r}".format(row[0],row[1]))
      
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
  put_parser.add_argument("-d", "--hide", action="store_true", help="Hide snippet from view.")
  put_parser.add_argument("-s", "--show", action="store_true", help="Allow snippet to be viewed.")
  
  # Subparser for "get" command
  logging.debug("Constructing <get> subparser...")
  get_parser = subparsers.add_parser("get", help="Retrieve a snippet.")
  get_parser.add_argument("name", type=str, 
                          help="Short name for snippet -- use double quotes to enclose spaces")
  
  # Subparser for "list" command
  logging.debug("Constructing <list> subparser...")
  list_parser = subparsers.add_parser("list", help="List all snippets (in alphabetical order).")
  
  # Subparser for "search" command
  logging.debug("Constructuing <search> subparser...")
  search_parser = subparsers.add_parser("search", help="Search all snippets for input string.")
  search_parser.add_argument("search_string", type=str, 
                             help="String to find -- use double quotes to enclose spaces.")
  
  arguments = parser.parse_args(sys.argv[1:])
  # Convert parsed arguments from namespace to dictionary
  arguments = vars(arguments)
  command = arguments.pop("command")
  
  if command == "put":
    name, snippet = put(**arguments)
  elif command == "get":
    snippet = get(**arguments)
  elif command == "list":
    list()
  elif command == "search":
    search(**arguments)
    
if __name__ == "__main__":
  main()
