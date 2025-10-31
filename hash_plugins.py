
import hashlib, glob
for f in glob.glob("minima/plugins/*.py"):
    h = hashlib.sha256(open(f,"rb").read()).hexdigest()
    print(f"{h} {f}")
