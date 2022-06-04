from fastapi import FastAPI
import github_downloader
from routerequest import req
from fastapi.responses import StreamingResponse
from starlette.background import BackgroundTasks
import os
import shutil

def remove_file(dir_name) -> None:
    os.remove(dir_name + ".zip")
    shutil.rmtree(dir_name)

app = FastAPI()

@app.get("/check")
def check():
    return {"hello","bye"}

@app.post("/url/{url}")
def  hello(Req:req, background_tasks: BackgroundTasks):
    url1 = Req.url
    url = url
    dir_name = github_downloader.run(url)

    def iterfile():  #

        with open(dir_name+".zip", mode="rb") as file_like:  #

            yield from file_like  #



    resp = StreamingResponse(iterfile(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={dir_name}'
    })

    background_tasks.add_task(remove_file, dir_name)
    return resp
