from lxml import etree
import argparse
from os import path
from pyaxmlparser import APK
from template import *
import subprocess
from shutil import move, rmtree, copytree
import re

NAME_ATTR = "{http://schemas.android.com/apk/res/android}name"

parser = argparse.ArgumentParser(prog="Container Generator", description="generate VirtualPatch container for an apk")
parser.add_argument('filename')
parser.add_argument('-o', '--output', required=False)
parser.add_argument('-i', '--input', help="folder containing the VirtualPatch Android Studio Project")

args = parser.parse_args()
if args.output is None:
  name = path.basename(args.filename).replace(".apk", "")
  args.output = f"{name}_container.apk"

apk = APK(args.filename)

manifest = apk.get_android_manifest_xml()
app_id = apk.get_package()
permissions = manifest.findall("uses-permission")

output_manifest = etree.fromstring(MANIFEST)

for p in permissions:
  output_manifest.append(p)

dir = args.input

rmtree(f"{dir}/containerlib", ignore_errors=True)
copytree(f"{dir}/lib",f"{dir}/containerlib")

# write custom lib manifest with right permissions
with open(f"{dir}/containerlib/AndroidManifest.xml", "wb") as out:
  out.write(etree.tostring(output_manifest, pretty_print=True))

# add appid to properties
with open(f"{dir}/gradle.properties", "r") as f:
  properties = f.read()

properties = re.sub(r"\nappid=.*", "", properties)

with open(f"{dir}/gradle.properties", "w") as f:
  f.write(f"{properties}\nappid=dev.sime1.container.{app_id}")

# add guest package info
with open(f"{dir}/container/build.gradle", "w") as f:
  f.write(GRADLE_SCRIPT.format(guest_package=app_id))

# change gradle settings to compile container
with open(f"{dir}/settings.gradle", "w") as f:
  f.write(GRADLE_SETTINGS)

# run gradle build (right now we compile the debug version, maybe we should compile the release one)
subprocess.run([f"./gradlew", "clean", "assembleDebug"], cwd=dir)
move(f"{dir}/container/build/outputs/apk/debug/container-debug.apk", args.output)