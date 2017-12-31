import os, sys
from dbnoterenderer import DanbooruPost, retrieveOrCacheJson, CONFIG
import argparse


def renderPool(poolid, fromid=False, toid=False, debug=False, innerdebug=False):
	pooldata = retrieveOrCacheJson(
		CONFIG.DOMAIN+"/pools/%d.json" % poolid,
		"cache/pool_%d.json" % poolid
	)
	posts = pooldata["post_ids"].split()

	os.makedirs("pool_%d" % poolid, exist_ok=True)

	enabled = True
	if fromid:
		fromid = int(fromid)
		enabled=False
	if toid:
		toid = int(toid)

	i = 0
	for postid in posts:
		i += 1
		postid = int(postid)

		if fromid and postid == fromid: enabled = True
		if toid and postid == toid: enabled = False
		if not enabled:
			continue

		if debug: print("Processing", i, "of", len(posts), "("+str(postid)+")")

		post = DanbooruPost(postid, debug=innerdebug)
		post.getData()
		post.render(("pool_%d/%03d_db%s." % (poolid, i, str(postid))) + post.getImageExtension() )


def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('poolid', metavar='POOLID', type=int, help='The pool ID')
	parser.add_argument('--from', dest='fromid', help='ID of the pool item to start processing from')
	parser.add_argument('--to', dest='toid', help='ID of the pool item to stop processing at')
	parser.add_argument('--debug', dest='debug', action="store_true", help='More output')

	args = parser.parse_args()

	try: poolid = int(args.poolid)
	except:
		print("No pool ID provided")
		return

	print("Downloading items in pool", poolid)
	print()
	renderPool(poolid, debug=True, fromid=args.fromid, toid=args.toid, innerdebug=args.debug)



if __name__ == '__main__':
	main()
