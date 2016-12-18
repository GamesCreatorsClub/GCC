

filename = "blah.txt" # input("FileName ~> ")
text_file = open(filename, "wt")

content = "First line \nSecond line\nAnd third" #input("File Contence ~>")

text_file.write(content)
text_file.close()