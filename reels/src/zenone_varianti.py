import sys,subprocess
src=open(sys.argv[1]).read(); out=sys.argv[2]
HIP='<path d="M395 300 C440 320 452 380 440 440 C432 480 412 500 380 505 L370 480 C395 470 405 450 410 420 C415 385 400 350 380 335 Z" fill="url(#skin)"/>'
SMILE='<path d="M282 250 C292 258 308 258 318 250" stroke="#F5F1E8" stroke-width="5" fill="none" stroke-linecap="round"/>'
assert HIP in src and SMILE in src
nomouth=src.replace(SMILE,'')
# pointing arm, drawn AFTER toga so it is in front: upper arm down, forearm forward/up, fist + index toward viewer
POINT='''<path d="M392 298 C432 310 452 350 456 400 C458 430 452 450 440 458 L410 446 C420 420 420 380 405 345 Z" fill="url(#skin)"/>
<path d="M418 440 C430 410 450 380 478 352 L506 380 C480 405 460 430 448 462 Z" fill="url(#skin)"/>
<ellipse cx="500" cy="352" rx="40" ry="36" fill="#E2AE84"/>
<path d="M470 360 C480 370 500 372 520 366 M474 340 C486 346 504 348 524 342" stroke="#B9805A" stroke-width="4" fill="none"/>
<path d="M470 352 C468 330 476 316 490 314 C504 312 512 326 510 346 Z" fill="#E9B88E"/>
<circle cx="489" cy="322" r="20" fill="#EDBF97" stroke="#B9805A" stroke-width="3"/>
<ellipse cx="489" cy="316" rx="10" ry="8" fill="#F6DCC4"/>
<path d="M466 372 C452 360 452 342 466 336" stroke="#B9805A" stroke-width="4" fill="none"/>'''
pointing=nomouth.replace(HIP,'').replace('<!-- belt -->',POINT+'\n<!-- belt -->')
pointing=pointing.replace('viewBox="0 0 600 1000"','viewBox="0 0 600 1000"')
for name,s in [('rest',nomouth),('point',pointing)]:
    open(f'{out}/z_{name}.svg','w').write(s)
    subprocess.run(['rsvg-convert','-h','760',f'{out}/z_{name}.svg','-o',f'{out}/z_{name}.png'],check=True)
