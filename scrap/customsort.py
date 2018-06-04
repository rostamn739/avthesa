if __name__ == "__main__":
	import sqlite3
	connection = sqlite3.connect( 'avthesa.db' )
	cu = connection.cursor( );
	
#	cu.execute('''
#ALTER TABLE WORDS_V2 ADD 
#ORD_ALPHA int(15) NOT NULL DEFAULT 0 
#	
#	''')
	
	cu.execute('''
SELECT query_for FROM WORDS_V2
	''')
	recs = cu.fetchall( )
	#print( recs )
	recs2 = [v[0] for v in recs]
	#print( recs2 )
	alphab = u"aāåąəə̄eēoōiīuūkxx́γcjtϑdδt̰pfbβŋŋ́nṇmyvrszšžš́ṣ̌h"
	recs3 = sorted(
		recs2,
		key=lambda wo: [alphab.index( c ) if c in alphab else 0 for c in wo])
	for k,v in enumerate( recs3 ):
		cu.execute( ''' 
UPDATE WORDS_V2 SET ORD_ALPHA = ?
WHERE query_for = ?
		
		''', (k+1,v))
		print( '%s is %s' % (k,v) )
	connection.commit( )
