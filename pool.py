import os, sys
from dbnoterenderer import DanbooruPost, retrieveOrCacheJson, CONFIG


def downloadPool(poolid, debug=False, innerdebug=False):
	pooldata = retrieveOrCacheJson(
		CONFIG.DOMAIN+"/pools/%d.json" % poolid,
		"cache/pool_%d.json" % poolid
	)
	posts = pooldata["post_ids"].split()

	os.makedirs("pool_%d" % poolid, exist_ok=True)

	i = 0
	for postid in posts:
		i += 1
		if debug: print("Processing", i, "of", len(posts), "("+postid+")")
		post = DanbooruPost(int(postid), debug=innerdebug)
		post.getData()
		post.render(("pool_%d/%03d_db%s." % (poolid, i, postid)) + post.getImageExtension() )


def main():
	try: poolid = int(sys.argv[1])
	except:
		print("No pool ID provided")
		return
	print("Downloading all items in pool", poolid)
	print()
	downloadPool(poolid, debug=True)



if __name__ == '__main__':
	main()
