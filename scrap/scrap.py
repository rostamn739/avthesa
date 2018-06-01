#!/usr/bin/env python3
import re;


def wordfiles_list( ):
	import glob
	return glob.glob( "temp/t12/*.html" )
	#return glob.glob( "temp/58269-vahi6101t5902m.html" )
	
class ParseResults:
	results_all = [ ]
	def __init__( self ):
		self.word_form = None;
		self.lemma = None;
		self.analyses = [ ];
		self.locations = [ ];
		#general query results
		self.query_for = u"";
		self.in_language = u"";
	def __str__( self ):
		return "wordform %s with lemma %s" % (self.word_form, self.lemma)
	
class _SearchCallbacks:
	pass
	#lemma = lambda string: string == u"Lemma:"
pass
cbacks = _SearchCallbacks	
	
class PersistCallbacks:
	def persist_one( self , r , cu):
		if r.query_for: r.query_for = str(r.query_for).strip( );
		else: r.query_for = None;
		if r.in_language: r.in_language = str(r.in_language).strip( );
		else: r.in_language = None;
		if not r.query_for: return;
		
		if r.word_form: r.word_form = str(r.word_form).strip( );
		else: r.word_form = None;
		if r.lemma: r.lemma = str(r.lemma).strip( );
		else: r.lemma = None;
		cu.execute('''INSERT INTO WORDS
VALUES (?, ?, ?, ?)
		''', (r.query_for, r.in_language, r.word_form, r.lemma));
		if r.locations:
			for l in r.locations:
				if not l: continue
				cu.execute('''INSERT INTO LOCATIONS
VALUES (?, ?)				
				''', (r.query_for, l.strip( )) );
		if r.analyses:
			for a in r.analyses:
				if not a: continue
				cu.execute('''INSERT INTO ANALYSES
VALUES (?, ?)
				''', (r.query_for, a.strip( )) );
pass
persist_one = PersistCallbacks( ).persist_one;
	
def parse( ):
	import bs4; bs = bs4.BeautifulSoup;
	for fil in wordfiles_list( ):
		resu = ParseResults( );
		with open( fil ) as f:
			soup = bs( f, "html.parser" )
			#print( soup )
			resu.lemma = ( soup.find_all(
				'td', string=re.compile(u"^Lemma") ) 
			)
			resu.word_form = ( soup.find_all( 
				'td',string=re.compile(u"^Word form") )
			)
			if len( resu.lemma ) > 0: #I don't know why this works
				resu.lemma = resu.lemma[ 0 ].next_sibling( )[ 0 ].string;
			if len( resu.word_form ) > 0:
				resu.word_form = resu.word_form[ 0 ].next_sibling.string;
			analyses = ( soup.find_all(
				'td', string=re.compile(u"^Analysis\\s+\\d") )
			)
			resu.analyses = map( lambda v: v.next_sibling.string ,
				analyses)
			#import pdb; pdb.set_trace( );
			resu.analyses = list( resu.analyses )
			locations = ( soup.find_all(
				'td', string=re.compile(u"^Location") )
			)
			resu.locations = map( lambda v: v.next_sibling( )[0].string ,
				locations)
			resu.locations = list( resu.locations )
			#general/fallback results
			resu.query_for = ( soup.find_all(
				'font', string=re.compile(u"^Query\\s+for") )
			)
			resu.in_language = ( soup.find_all(
				'font', string=re.compile(u"^in\\s+language") )
			)
			#import pdb; pdb.set_trace( );
			if len( resu.query_for ) > 0:
				resu.query_for = \
					resu.query_for[ 0 
						].parent.next_sibling.next_sibling.findAll(
						text=True )
				_t = [ ];
				for i in resu.query_for:
					_t.append( str( i ) )
				resu.query_for = ("".join( _t )).split( )
				resu.query_for = u' '.join( resu.query_for );
			if len( resu.in_language ) > 0:
				resu.in_language = \
					resu.in_language[ 0 
						].parent.next_sibling.next_sibling.findAll(
						text=True )
				_t = [ ];
				for i in resu.in_language:
					_t.append( str( i ) )
				resu.in_language = ("".join( _t )).split( )
				resu.in_language = u' '.join( resu.in_language );
		print( resu );
		persist_one( resu );
		print( "resu persisted with count %s" % len( ParseResults.results_all ) )
		#print( "With analyses %s" % resu.analyses )
		#print( "With locations %s" % resu.locations )
		#print( "With fallback to %s in %s" % (resu.query_for, resu.in_language) )
		ParseResults.results_all.append( resu )
	print( "]]resu count %s" % len( ParseResults.results_all ) )
	return ParseResults.results_all;
	
def persist( resu ):
	def populate_WORDS( ):
		for r in resu:
			pass
	populate_WORDS( );

if __name__ == "__main__":
	import sqlite3
	connection = sqlite3.connect( 'avthesa.db' )
	cu = connection.cursor( );
	def create_WORDS( ):
		#cu.execute( "DROP TABLE IF EXISTS WORDS " );
		cu.execute( '''CREATE TABLE WORDS (
QUERY_FOR text not null,
IN_LANGUAGE text null,
WORD_FORM text null,
LEMMA text null
		)''' );
	#create_WORDS( );
	def create_LOCATIONS( ):
		#cu.execute( "DROP TABLE IF EXISTS LOCATIONS" );
		cu.execute( '''CREATE TABLE LOCATIONS (
WORD_QUERY_FOR text not null,
LOCATION text not null
		)''');
	#create_LOCATIONS( );
	def create_ANALYSES( ):
		#cu.execute( "DROP TABLE IF EXISTS ANALYSES" );
		cu.execute( '''CREATE TABLE ANALYSES (
WORD_QUERY_FOR text not null,
ANALYSIS text not null
		)''');
	#create_ANALYSES( )
	from functools import partial;
	persist_one = partial(persist_one, cu=cu)
	
	resu = parse( );
	print ( "]]got resu with count %s " % len( resu ) );
	connection.commit( )
	connection.close( )
	#persist( resu );
	
