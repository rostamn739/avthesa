const puppe = require( 'puppeteer' );

( async () => {
	const browser = await puppe.launch( 
{headless: false, slowMo: 130, args: [ '--no-sandbox', '--disable-setuid-sandbox' ]} );
	const page = await browser.newPage( );
	await page.goto( 
'http://titus.uni-frankfurt.de/texte/etcs/iran/airan/avesta/avest.htm' );
	//let avframe = page.frames( )[0].childFrames( )[0];
	//console.log( await avframe.content() );
	//for (let wordlink of await avframe.$$( 'a[href^="javascript:ci"]' )) {
	//	//console.log( wordlink );
	//	await wordlink.click( );
	//}
	const lvl2frame = page.frames( )[3].childFrames( )[0];
	const lvl3frame = page.frames( )[3].childFrames( )[1];
	let el = await lvl2frame.$( 'select[name^="TT2"]' );
	if (el != null) console.log( el );
	el = await lvl2frame.$( 'select[name^="TT3"]' );
	if (el != null) console.log ( el );
})( );
