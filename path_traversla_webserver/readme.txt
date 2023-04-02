You are given a web server that has a vulnerable API endpoint that allows you to submit a query parameter,
Your goal is to enhance security measures to prevent the use of path traversal techniques to manipulate
the query parameter and access files outside of the intended directory.

i.e "/image?filename=../../../etc/passwd" should return a HTTP response code = 401