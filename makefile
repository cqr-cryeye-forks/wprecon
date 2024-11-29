build:
	go build -gcflags=all=-e .
	chmod +x wprecon
	mv wprecon /usr/local/bin
