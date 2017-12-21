import os
import click
from .config import Palette
from .service import picture, website
from .server import start
from .benchmark import profile

CONTEXT_SETTINGS = dict(obj={})


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--colors', '-C', type=click.Path(exists=True), nargs=1,
    help='Path to Color palette file')
@click.option(
    '--width', '-W', type=int, nargs=1, default=30,
    help='Number of boxes wide for boxelized image')
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.pass_context
def cli(ctx, colors, width, verbose):
    """
    \b
        __                    __
       / /_  ____  _  _____  / /
      / __ \/ __ \| |/_/ _ \/ /
     / /_/ / /_/ />  </  __/ /
    /_.___/\____/_/|_|\___/_/


    CLI interface for boxel codec

    """
    ctx.obj['WIDTH'] = width
    if colors:
        ctx.obj['PALETTE'] = Palette(file=colors)
    else:
        ctx.obj['PALETTE'] = colors


@cli.command('img', short_help='Boxelizes images', help='Usage: boxel img [image files...]')
@click.argument('src', type=click.Path(exists=True), nargs=-1, required=True)
@click.option(
    '--output', '-O', type=click.Path(writable=True), nargs=1,
    help='File destination for boxelized image.')
@click.pass_context
def img(ctx, src, output):
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        for img_file in src:
            base = os.path.basename(img_file)
            filename = os.path.splitext(base)[0] + '.png'
            boxel_it = picture(ctx.obj['WIDTH'],
                               img_file, palette=ctx.obj['PALETTE'])
            boxel_im.save(output + filename, 'PNG')
    else:
        for img_file in src:
            picture(ctx.obj['WIDTH'],
                    img_file, palette=ctx.obj['PALETTE'])[0].show()


@cli.command('web', short_help='Boxelizes a website',
        help='Usage: boxel web [urls...]')
@click.argument('urls', nargs=-1, required=True)
@click.option(
    '--output', '-O', type=click.Path(writable=True),
    help='File destination for boxelized website image files.')
@click.pass_context
def web(ctx, urls, output):
    if output:
        if not os.path.exists(output):
            os.makedirs(output)
        for url in urls:
            base = os.path.basename(img_file)
            filename = os.path.splitext(base)[0] + '.png'
            boxel_im = website(ctx.obj['WIDTH'],
                               url, palette=ctx.obj['PALETTE'])
            boxel_im.save(output + filename, 'PNG')
    else:
        for url in urls:
            website(ctx.obj['WIDTH'],
                    url, palette=ctx.obj['PALETTE'])[0].show()


@cli.command(
    'video', short_help='Boxelizes video setting up a streaming service',
    help='Usage: boxel video -R [redis] -U [websocket] --Realm [room]')
@click.option('--redis', '-R', nargs=1, help='URL of Redis DB')
@click.option(
    '--URL', '-U', nargs=1, default='ws://localhost:8080/ws',
    help='URL of the websocket')
@click.option(
    '--Realm', nargs=1, default='boxel', help='Name of the room to join')
@click.option(
    '--benchmark/--no-benchmark', is_flag=True,
    help='Profile while executing a command')
@click.pass_context
def stream(ctx, redis, url, realm, benchmark):
    click.echo('Starting up web streaming service.')
    url = u'%s' % url
    realm = u'%s' % realm
    if benchmark:
        click.echo('Profiling....')
        profile(url, ctx.obj['WIDTH'], redis, ctx.obj['PALETTE'], realm)
    else:
        start(url, ctx.obj['WIDTH'], redis, ctx.obj['PALETTE'], realm)

if __name__ == '__main__':
    cli()
