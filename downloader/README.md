#### some research about download something about python
##### library
* urllib: urllib has no cookie support, HTTP/FTP/local files only (no SSL)
* urllib2: complete HTTP/FTP client, supports most needed things like cookies, does not support all HTTP verbs (only GET and POST, no TRACE, etc.)
* urllib3 - supports connection re-using/pooling and file posting. Deprecated (a.k.a. use urllib/urllib2 instead)
* httplib - HTTP/HTTPS only (no FTP)
* httplib2 - HTTP/HTTPS only (no FTP)

* mechanize: can use/save Firefox/IE cookies, take actions like follow second link, actively maintained (0.2.5 released in March 2011)
* PycURL: supports everything curl does (FTP, FTPS, HTTP, HTTPS, GOPHER, TELNET, DICT, FILE and LDAP), bad news: not updated since Sep 9, 2008 (7.19.0)
* requests: urllib for human.
