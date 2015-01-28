import argparse
import logging
import sys

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log",level=logging.DEBUG)

def put(name, snippet):
  """
  Store a snippet with an associated name.
  
  Returns the name and the snippet.
  """
  logging.error("FIXME: Unimplemented - put({!r}, {!r})").format(name, snippet)
  return name, snippet

def get(name):
  """
  Retrieve the snippet with a given name.
  
  If there is no such snippet... return false.
  
  Returns the snippet.
  """
  logging.error("FIXME: Unimplemented - get({!r})").format(name)
  return snippet or False

def list():
  """
  Return a list of snippet names
  """
  logging.error("FIXME: Unimplemented - list()")
  pass # return names as list for display/printing?

def main():
  """Main function"""
  logging.info("Constructing parser...")
  parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
  parser.add_argument("mode", help="Choose one from:  get, put, list")
  parser.add_argument("name", help="Short name for snippet (no spaces)")
  parser.add_argument("snippet", help="Snippet to store -- use double quotes to enclose spaces")
  arguments = parser.parse_args(sys.argv[1:])
  #print arguments.mode

if __name__ == "__main__":
  main()
