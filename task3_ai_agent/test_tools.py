from tools import web_search, calculator, read_file

print(calculator.invoke("(25 * 4) + 10 / 2"))
print(read_file.invoke("notes.txt"))
print(web_search.invoke("capital of Australia")[:300])