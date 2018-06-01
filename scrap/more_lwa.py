import re


def wordfiles_list( ):
    import glob
    return glob.glob( "temp/t23/*.html" )
    #return glob.glob( "temp/58269-vahi6101t5902m.html" )

class PersistCallbacks:
    def persist_one( self, r, cu):
        if not r[ 'query_for' ]: return;
        if r[ 'analyses' ]:
            for a in r[ 'analyses' ]:
                if not a: continue;
                if a == 'Thesaurus entry not found!': continue;
                cu.execute('''INSERT INTO ANALYSES
VALUES (?, ?)
                ''', (r[ 'query_for' ], a.strip( )) );
        if r[ 'locations' ]:
            for l in r[ 'locations' ]:
                if not l: continue;
                cu.execute('''INSERT INTO LOCATIONS
VALUES (?, ?)               
                ''', (r[ 'query_for' ], l.strip( )) );
        print( "Inserted %s loca & %s ana FOR %s" % (
            len( r['locations'] ), len ( r['analyses'] ), r['query_for']) )
                
pass
persist_one = PersistCallbacks( ).persist_one;


class Aux:
    def print_resu( self, resu ):
        print("]]]]]]]]]]]]]]]]]]")
        print( "Analyses are: %s" % resu[ 'analyses' ] )
        print( "- -" )
        print( "Locations are: %s" % resu[ 'locations' ] )
        print( "- -" )
        print( "Is ALL for query form %s" % resu[ 'query_for' ] )
        print( "[[[[[[[[[[[[[[[[[" ) 
pass
print_resu = Aux( ).print_resu

def parse( ):
    import bs4; bs = bs4.BeautifulSoup;
    for fil in wordfiles_list( ):
        resu = {    "analyses":[ ],
                    "locations":[ ],
                    "word_forms":[ ],
                    "query_for":None }
        with open( fil ) as f:
            soup = bs( f, "html.parser" )
            tables = soup.find_all(
                'table', border="1" )
            #print( len(tables) )
            for t in tables:
                analysis = t.find_all(
                    'tr', bgcolor="#ffffff" )
                for a in analysis:
                    if a:
                        a = a.find_all( text=True )
                        a = ("".join( a )).split( )
                        a = u' '.join( a )
                        #print( a )
                        resu[ 'analyses' ].append( a )
                #analyses done
                rows = t.find_all(
                    'tr', bgcolor="#ddffdd" ) \
                    + \
                    t.find_all(
                    'tr', bgcolor="#cceecc" )
                for r in rows:
                    if r:
                        cells = r.find_all( 'td' )
                        if len( cells ) > 1:
                            word_form = cells[ 1 ].find_all( text=True )
                            word_form = ("".join( word_form )).split( )
                            word_form = u' '.join( word_form )
                            resu[ 'word_forms' ].append( word_form )
                        if len( cells ) > 3:
                            loca = cells[ 3 ].find_all( text=True )
                            loca = ("".join( loca )).split( )
                            loca = u' '.join( loca )
                            resu[ 'locations' ].append( loca )
                #word_forms and locations done
            query_for = ( soup.find_all(
                'font', string=re.compile(u"^Query\\s+for") )
            )
            if len( query_for ) > 0:
                query_for = \
                    query_for[ 0 
                        ].parent.next_sibling.next_sibling.findAll(
                        text=True )
                _t = [ ];
                for i in query_for:
                    _t.append( str( i ) )
                query_for = ("".join( _t )).split( )
                query_for = u' '.join( query_for );
            resu[ 'query_for' ] = query_for;
        #print_resu( resu )
        persist_one( resu )



if __name__ == "__main__":
    import sqlite3
    connection = sqlite3.connect( 'avthesa.db' )
    cu = connection.cursor( );
    
    from functools import partial;
    persist_one = partial(persist_one, cu=cu)
    
    parse( )
    
    connection.commit( )
    connection.close( )















