from fastapi import FastAPI
import github_downloader
from routerequest import req
from fastapi.responses import StreamingResponse
from fastapi.responses import HTMLResponse
from starlette.background import BackgroundTasks
import os
import shutil

app = FastAPI()

def remove_file(dir_name) -> None:
    os.remove(dir_name + ".zip")
    shutil.rmtree(dir_name)




@app.get("/",response_class=HTMLResponse)
def start_page():
    fi_html = open("README.html","r")
    data = fi_html.read()
    fi_html.close()
    return  data



@app.get("/check")
def check():
    return {"hello","bye"}


@app.post("/get_add")
def get_add(REQ: req):
    url = REQ.url
    dir_name = github_downloader.run(url)
    

    return dir_name



@app.get("/download/{name}")
def download(name:str, background_tasks: BackgroundTasks):
    dir_name = name
    def iterfile():
        
        with open(dir_name+".zip",mode='rb') as file_like:

            yield from file_like

    resp = StreamingResponse(iterfile(), media_type="application/x-zip-compressed", headers={                                   
           'Content-Disposition': f'attachment;filename={dir_name}'                                                                
       })
    
    background_tasks.add_task(remove_file, dir_name)
    return resp




@app.get("/url/{url1}")
def  hello(url1: str, background_tasks: BackgroundTasks):
    #url1 = Req.url
    url = github_downloader.per20(url1)
    dir_name = github_downloader.run(url)

    def iterfile():  #

        with open(dir_name+".zip", mode="rb") as file_like:  #

            yield from file_like  #



    resp = StreamingResponse(iterfile(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={dir_name}'
    })

    background_tasks.add_task(remove_file, dir_name)
    return resp
