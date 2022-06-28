from glob import glob
import os
pre = "yes-"
[os.rename(f, "{}{}".format(pre, f)) for f in glob("*.jpg")]