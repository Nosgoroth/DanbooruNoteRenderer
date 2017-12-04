# DanbooruNoteRenderer

Developed in a few hours because I don't have the patience to typeset, and provided in the hopes that it's useful to someone, maybe as a starting point for a proper typeset or as a low-effort typeset for whatever reason. As an example, [this post](http://danbooru.donmai.us/posts/2836730?pool_id=12768) becomes [this image](https://i.imgur.com/3kcbtho.png).

Not in active development, but feel free to fork or pull request.

## Requisites

**Python 3.2+**. Depends on requests, pillow and imgkit, which itself requires wkhtmltox installed. Developed and tested on macOS 10.13.

## Usage

Use from CLI or include inside your project and do whatever, see the `main()` methods for more.

### Render a single post

Run `python3 dbnoterenderer.py 2836730` (a post id) to render a single post. You may need to create a folder named `output` for it to work.

When including the code:

```py
from dbnoterenderer import DanbooruPost

post = DanbooruPost(2836730, debug=True)
post.getData()
post.render(output="mytest.png")
```

### Render a pool

Run `python3 pool.py 12768` (a pool id) to render all posts in a pool. It will create a `pool_12768` folder.

When including the code:

```py
from pool import renderPool

renderPool(12768, debug=True, innerdebug=False)
```

## Cache

To limit accesses to Danbooru API, the JSON results of the API calls as well as the original downloaded images are kept in a folder named `cache`. Delete it to redownload things, or use the images there if you want to composite a better typeset by combining them with the rendered image and some manual touches.

