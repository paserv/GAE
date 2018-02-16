from os import listdir
from os.path import isfile, join

mypath = '.'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
output = open("index.html","w") 

for file in onlyfiles:
   if file != "get_files.py" and file != "index.html":
      print file
      output.write("<img style='vertical-align:middle' onclick='copy(\"" + file + "\")' src='" + file + "' height='100' width='100' title='" + file + "'>")

output.write("<script>function copy(filename) { var tempInput = document.createElement('input'); tempInput.style = 'position: absolute; left: -1000px; top: -1000px'; tempInput.value = filename; document.body.appendChild(tempInput); tempInput.select(); document.execCommand(\"Copy\"); document.body.removeChild(tempInput);} </script>")
output.close()
