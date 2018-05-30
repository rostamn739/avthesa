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
	let lvl2 frame = page.frames( )[1].childFrames( )[0];
	let lvl3 frame = page.frames( )[1].childFrames( )[1];
	
})( );
