lines = [ ]

with open( "fehler" ) as fihler:
	lines = fihler.readlines( )
	
for line in lines:
	afs = line.rsplit( '/', 1 )
	afs = afs[ -1 ]
	befd = afs.split( '-' )
	befd = befd[ 0 ]
	#print( befd )
	afd = afs.split( '-' )[ 1 ]
	if ".html" in afd:
		#print( afd )
		pass
	word = afd.split( ".html")
	word = word[ 0 ]
	#print( word )
	lang = befd;
	print( "javascript:ci(%s,'%s')" % (lang, word) );
