if __name__ == "__main__":
	import sqlite3
	connection = sqlite3.connect( 'avthesa.db' )
	cu = connection.cursor( );
	
	cu.execute('''
CREATE TABLE IF NOT EXISTS WORDS_V2 (
QUERY_FOR text not null,
IN_LANGUAGE int(2) not null,
WORD_FORM text null,
LEMMA text null,
PRIMARY KEY (QUERY_FOR, IN_LANGUAGE)
)
	''');
	cu.execute('''
CREATE TABLE IF NOT EXISTS LOCATIONS_V2 (
QUERY_FOR text not null,
LOCATION text not null
)	
	''');
	cu.execute('''
CREATE TABLE IF NOT EXISTS ANALYSES_V2 (
QUERY_FOR text not null,
ANALYSIS text not null

)
	''');
	
	cu.execute('''
CREATE TABLE IF NOT EXISTS ANALYSES_T2 (
query_for text not null,
analysis text not null
)
	''')
	
	cu.execute('''
CREATE TABLE IF NOT EXISTS LOCATIONS_T2 (
query_for text not null,
location text not null
)
	''')
	
	cu.execute('''
INSERT INTO LOCATIONS_T2 
SELECT * FROM LOCATIONS
	''')
	
	cu.execute('''
INSERT INTO ANALYSES_T2
SELECT * FROM ANALYSES
	''')
	
	cu.execute('''
SELECT query_for, in_language,
word_form, lemma
 FROM WORDS ORDER BY QUERY_FOR

	''');
	
	words = cu.fetchall( )
	
	for w in words:
		qf = w[0];
		inl = w[1];
		wf = w[2]
		lem = w[3]
		if not qf: continue;
		
		qf_s = qf.split(u'.')
		#if not ( u'.'.join( qf_s ) ) == qf:
		#	print(qf)
		qf_s2 = []; import re;
		for v in qf_s:
			qf2 = v;
			qf2 = re.sub(u"tk", u"t̰k", qf2)
			qf2 = re.sub(u"^tb", u"t̰b", qf2)
			if ( re.search( u'st$', qf2 ) ) or \
				( re.search( u'št$', qf2 ) ):
					pass
			else:
				qf2 = re.sub(u't$', u't̰', qf2)
			qf_s2.append(qf2)
		qf_2 = u'.'.join( qf_s2 )
		if not qf == qf_2: print( "%s is %s" % (qf, qf_2) )
		#else: print( '%s is normal' % (qf) );
		#import pdb; pdb.set_trace( )
		if (re.search( u'old', inl)):
			inl = 1;
		elif (re.search( u'young', inl)): 
			inl = 2;
		else: inl = 3
		
		try:
			cu.execute('''
INSERT INTO WORDS_V2 (Query_for, in_language,
word_form, lemma) VALUES (?,?,?,?)	
		
			''', (qf_2, inl,wf, lem))
		except sqlite3.Error as e:
			print( "SQLITE ERROR: %s" % (e) )
		cu.execute('''
UPDATE LOCATIONS_T2 SET Query_for = ?
WHERE QUERY_FOR = ?
		''', (qf_2, qf) )
		cu.execute('''
UPDATE ANALYSES_T2 SET query_for = ?
WHERE query_for = ?
		''', (qf2, qf))
		
	connection.commit( )
		
