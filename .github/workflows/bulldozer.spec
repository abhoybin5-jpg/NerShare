[app]
title = NetShare
package.name = netshare
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.1.0.cython=0.29.33
orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
