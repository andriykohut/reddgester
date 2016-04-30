import asyncio
import click
import ujson

from aiohttp import web
from nameko.standalone.rpc import ClusterRpcProxy


@asyncio.coroutine
def trigger_digest(request):
    data = yield from request.json(loader=ujson.loads)
    with ClusterRpcProxy(request.app['RPC_CONFIG']) as cluster_rpc:
        cluster_rpc.reddit_digester.digest.async(
            data['r'],
            int(data.get('limit', 10)),
            data['to']
        )
    return web.json_response({'triggered': 1}, dumps=ujson.dumps)


@click.group()
def cli():
    pass


@click.command()
@click.option('--host', default='0.0.0.0', help='api hostname.',
              show_default=True)
@click.option('--port', default=8080, help='api portnumber.',
              show_default=True)
@click.option('--amqp-uri', help='url for digester RPC.', required=True)
def runserver(host, port, amqp_uri):
    app = web.Application()
    app['RPC_CONFIG'] = {
        'AMQP_URI': amqp_uri
    }
    app.router.add_route('POST', '/trigger_digest', trigger_digest)
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    cli.add_command(runserver)
    cli()
