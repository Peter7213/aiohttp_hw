from aiohttp import web
from db import init_orm, close_orm, Ad, Session
from sqlalchemy.ext.asyncio import AsyncSession
import json
from schema import CreateAd, UpdateAd
import pydantic
from sqlalchemy import select


def validate(incoming_json: dict, schema: type[CreateAd | UpdateAd]):
    try:
        return schema(**incoming_json).model_dump(exclude_unset=True)
    except pydantic.ValidationError as err:
        raise get_error(web.HTTPBadRequest, str(err))


async def orm_context(app: web.Application):
    await init_orm()
    yield
    await close_orm()

@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response

app = web.Application()
app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

def get_error(
    error_cls: type[web.HTTPNotFound | web.HTTPBadRequest], message: dict | list | str
):
    error_message = {"error": message}
    error_message_json = json.dumps(error_message)
    return error_cls(text=error_message_json, content_type="application/json")

class AdView(web.View):

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    @property
    def ad_id(self) -> int:
        return int(self.request.match_info['ad_id'])

    async def get_ad(self) -> Ad:
        ad = await self.session.get(Ad, self.ad_id)
        if ad is None:
            raise get_error(web.HTTPNotFound, "ad with this ID not found")
        return ad

    async def get(self):
        ad_id = self.request.match_info.get('ad_id')
        if ad_id:
            ad = await self.session.get(Ad, int(ad_id))
            if ad is None:
                raise get_error(web.HTTPNotFound, "ad with this ID not found")
            return web.json_response(ad.dict)
        else:
            result = await self.session.execute(select(Ad))
            ads = result.scalars().all()
            return web.json_response([ad.dict for ad in ads])


    async def post(self):
        json_data = validate(await self.request.json(), CreateAd)
        ad = Ad(
            header=json_data['header'],
                ad_body=json_data['ad_body'],
                owner=json_data['owner']
        )
        self.session.add(ad)
        await self.session.commit()
        return web.json_response(ad.dict, status=201)

    async def patch(self):
        json_data = validate(await self.request.json(), UpdateAd)
        ad = await self.get_ad()
        if "header" in json_data:
            ad.header = json_data['header']
        if "ad_body" in json_data:
            ad.ad_body = json_data['ad_body']
        self.session.add(ad)
        await self.session.commit()
        return web.json_response(ad.dict)

    async def delete(self):
        ad = await self.get_ad()
        await self.session.delete(ad)
        await self.session.commit()
        return web.json_response({'status': 'ad deleted'})


app.add_routes(
    [
        web.get('/ads', AdView),
        web.post('/ads', AdView),
        web.get(r'/ads/{ad_id:\d+}', AdView),
        web.patch(r'/ads/{ad_id:\d+}', AdView),
        web.delete(r'/ads/{ad_id:\d+}', AdView)
     ]
)
web.run_app(app)