import azure.functions as func


from fastapi import FastAPI
import github_downloader
from routerequest import req
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.background import BackgroundTasks
import os
import shutil

app = FastAPI()


def remove_file(dir_name) -> None:
    os.remove(dir_name + ".zip")
    shutil.rmtree(dir_name)





@app.get("/check")
def check():
    return {"hello", "bye"}


@app.post("/get_add")
def get_add(REQ: req):
    url = REQ.url
    dir_name = github_downloader.run(url)

    return dir_name

@app.get("/gitdl/")
def gitdl(link:str):
    print("git_dl")
    if link is not None:
        dir_name = github_downloader.run(link)
        response = RedirectResponse("download/"+dir_name)
        return response


@app.get("/download/{name}")
def download(name: str, background_tasks: BackgroundTasks):
    dir_name = name

    def iterfile():
        with open(dir_name + ".zip", mode='rb') as file_like:
            yield from file_like

    resp = StreamingResponse(iterfile(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={dir_name}'
    })

    background_tasks.add_task(remove_file, dir_name)
    return resp




@app.get("/url/")
def hello(link: str, background_tasks: BackgroundTasks):
    # url1 = Req.url
    #url = github_downloader.per20(url1)
    url = link
    dir_name = github_downloader.run(url)

    def iterfile():  #

        with open(dir_name + ".zip", mode="rb") as file_like:  #

            yield from file_like  #

    resp = StreamingResponse(iterfile(), media_type="application/x-zip-compressed", headers={
        'Content-Disposition': f'attachment;filename={dir_name}'
    })

    background_tasks.add_task(remove_file, dir_name)
    return resp

@app.get("/")
async def strat_page():
    response = RedirectResponse("/index.html")
    return response
#for website data
app.mount("/", StaticFiles(directory="website"),name="web")

app = func.AsgiFunctionApp(app=app,
                           http_auth_level=func.AuthLevel.ANONYMOUS)

