# DanbooruNoteRenderer

Developed because I don't have the patience to typeset, and provided in the hopes that it's useful to someone, maybe as a starting point for a proper typeset or as a low-effort typeset for whatever reason. As an example, [this post](http://danbooru.donmai.us/posts/2836730?pool_id=12768) becomes [this image](https://i.imgur.com/3kcbtho.png).

**Python 3.2+**. Depends on requests, pillow and imgkit, which itself requires wkhtmltox installed. Developed and tested on macOS 10.13.

Usage: `python3 dbnoterenderer.py 2836730` (a post id) to render a single post, `python3 pool.py 12768` (a pool id) to render all posts in a pool. Or include inside your project and do whatever, see the `main()` methods for more.