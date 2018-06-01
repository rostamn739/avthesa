
const puppe = require( 'puppeteer' );
const fs = require( 'fs' );

let openword = async (lang, word) => {
	let aa = lang; let bb = word;
	const URI = ("http://titus.uni-frankfurt.de/database/titusinx/titusinx.asp?LXLANG="+
		aa+"&LXWORD="+
		bb+"&LCPL=0&TCPL=0&C=H&PF=13");
	const page = await (await puppe.launch( 
{headless: false, slowMo: 250, args: [ '--no-sandbox', '--disable-setuid-sandbox' ]} ).newPage( ));
	
	await page.goto(URI);
	fs.writeFileSync( 'temp/'+word+'.html', page.content( ) );
}

( async () => {
	const browser = await puppe.launch( 
{headless: false, slowMo: 220, args: [ '--no-sandbox', '--disable-setuid-sandbox' ]} );
	const page = await browser.newPage( );
	//await page.goto( 
	//'http://titus.uni-frankfurt.de/texte/etcs/iran/airan/avesta/avest.htm' );
	let hreflines = fs.readFileSync( '../labour/hrefslist_uniq3.txt' 
		).toString( ).match(/^.+$/gm);
	for (let hline of hreflines) {
		lang = hline.split( '(' )[ 1 ].split( ',' )[ 0 ];
		word = hline.split( ',' )[ 1 ].split( ')' )[ 0 ];
		lang = lang.trim( );
		word = word.trim( ).replace( /^'(.*)'$/ ,'$1');
		//console.log (lang);
		//console.log (word);
		let aa = lang; let bb = word;
		let uri = ("http://titus.uni-frankfurt.de/database/titusinx/titusinx.asp?LXLANG="+
aa+"&LXWORD="+
bb+"&LCPL=0&TCPL=0&C=H&PF=13");
		await page.goto( uri );
		//await page.waitForNavigation( );
		fs.writeFileSync( 'temp/'+lang+'-'+word+'.html', await page.content( ) );
		{let stream = fs.createWriteStream(
			"append.txt",
			{flags: 'a'});
		stream.write( hline + "\n" );
		stream.end( );}
	}
})( );
