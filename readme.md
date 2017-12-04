# DanbooruNoteRenderer

Renders all notes in a Danbooru post into its image, including HTML styles.

Developed in a few hours because I don't have the patience to typeset. As an example, [this post](http://danbooru.donmai.us/posts/2836730?pool_id=12768) becomes [this image](https://i.imgur.com/3kcbtho.png).

_Definitely_ don't expect the results to be anywhere near perfect. With luck they'll be readable, but sometimes you might find textboxes overlapping each other or other undesired results. The output of this script could be used as a starting point for a proper typeset, or as a low effort low quality typeset if you really want a typeset but none exists and you can't be bothered to do it yourself.

Not in active development, but feel free to fork or pull request.

## Requisites

**Python 3.2+**. Depends on requests, pillow and imgkit, which itself requires wkhtmltox installed. Maybe install the "Wild Words" font too.

Developed and tested on macOS 10.13.

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


## Styles

Edit `DanbooruNote.render` to make changes. Currently uses `font family: "Wild Words", sans-serif;` as default, but will use any font declared in the html of the note if it's installed in your system.

## Cache

To limit accesses to Danbooru API, the JSON results of the API calls as well as the original downloaded images are kept in a folder named `cache`. Delete it to redownload things, or use the images there if you want to composite a better typeset by combining them with the rendered image and some manual touches.

## FAQ

### It's slow!

Yyyyep. Calling the `wkhtmltoimage` binary to render the html of each and every note will do that. Then again, it doesn't bother me too much.

### Hyphenation?

That would be cool, yes. My `wkhtmltoimage` binary isn't listening to `hyphens: auto;`, though, so if you have a better idea, please go ahead and pull request.

### Maybe check for textbox overlapping?

Certainly a possibility, and I considered it, but this was a three hour project to render a pool because I couldnt be bothered to manually typeset it myself. You could definitely do something with the coordinates in `DanbooruPost.renderNotes`. Don't let me stop you.

