#!/usr/bin/env python3

from litestar import Litestar, get, post
from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import (
    ScalarRenderPlugin,
    RapidocRenderPlugin,
    RedocRenderPlugin,
    SwaggerRenderPlugin,
)

from enhanced_discord_bot_llms.llm_svc import (
    LLMModel,
    gen_async_client,
    UserInfo,
    streaming_usine_de_gaou_creation,
)


@get("/", sync_to_thread=False)
def read_root() -> dict:
    return {"Hello": "World"}


@post("/gaou/{parametre:str}")
async def creer_gaou(parametre: str) -> UserInfo:
    model = LLMModel.LLAMA3
    client = gen_async_client(model=model)
    gaou = await streaming_usine_de_gaou_creation(client, parametre, model=model)
    print(f"Nouveau gaou créé: {gaou},\n selon le paramètre {parametre}\n\n")
    return gaou


app = Litestar(
    route_handlers=[read_root, creer_gaou],
    openapi_config=OpenAPIConfig(
        title="Gaou API",
        description="API pour créer des Gaous",
        version="0.1.0",
        path="/docs",
        render_plugins=[
            RapidocRenderPlugin(),
            # RedocRenderPlugin(),
            # ScalarRenderPlugin(),
            # SwaggerRenderPlugin(),
        ],
    ),
    debug=True,
)

if __name__ == "__main__":
    import uvicorn

    application = "gaouapp:app"
    uvicorn.run(application, host="0.0.0.0", port=8000, reload=True)
