Optional: real three.js for the 3D preview
==========================================
The app works without this. It uses its own small 3D engine (static/mini3d.js) unless a real three.js build is here.

1. Put a three.js build named three.min.js in this folder. Use release r128 (it is a plain script that defines a global THREE):

     curl -fL -o three.min.js https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js
   or: wget -O three.min.js https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js

2. Check it is real: it must be about 600 KB, not 0 bytes, and the first line should mention threejs.org.

     ls -l three.min.js
     head -c 120 three.min.js

3. Restart the app (./run.sh) and reload the page. The line at the bottom left of the 3D view says "three.js"
   when it is used, and "built-in engine" when it is not. If three.js fails for any reason the app switches back
   to the built-in engine by itself, and the browser console (F12) says why.

Newer three.js releases (r160 and later) no longer ship a plain three.min.js, so use r128 or a similar older build.
