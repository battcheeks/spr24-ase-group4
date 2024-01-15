# ----------------------------------------------------------------------------
# Utility Class for helper functions such as csv reader, etc.
import ast
import re, fileinput

class Utitlity:
  def __init__(self) -> None:
    pass

  def l_csv(self, file="-"):
    with  fileinput.FileInput(None if file=="-" else file) as src:
      for line in src:
        # This regex replaces all the characters in bracket and words starting with #. with an empty string.
        line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
        # Then we feed the commma seperated data values to coerce for type conversion.
        if line: yield [self.l_coerce(x) for x in line.split(",")]
  
  def l_coerce(self, x):
    # literal_eval will convert the string to appropriate data type and the exception is when x is a string.
    try : return ast.literal_eval(x)
    except Exception: return x.strip()