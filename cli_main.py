from github_downloader import run
import sys

if len(sys.argv) > 1:
    url = sys.argv[1]
    run(url)
else:
    print("Enter a github repo")
