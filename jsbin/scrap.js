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
{headless: false, slowMo: 250, args: [ '--no-sandbox', '--disable-setuid-sandbox' ]} );
	const page = await browser.newPage( );
	await page.goto( 
'http://titus.uni-frankfurt.de/texte/etcs/iran/airan/avesta/avest.htm' );
	//console.log( await avframe.content() );
	//for (let wordlink of await avframe.$$( 'a[href^="javascript:ci"]' )) {
	//	//console.log( wordlink );
	//	await wordlink.click( );
	//}
	
	const lvl2frame = page.frames( )[3].childFrames( )[0];
	const lvl3frame = page.frames( )[3].childFrames( )[1];
	let booksel = await lvl2frame.$( 'select[name^="TT2"]' );
	let chaptsel = await lvl3frame.$( 'select[name^="TT3"]' );
	
	for (let book of await booksel.$$( 'option' )) {
		//await page.waitForNavigation( );
		let chaptsel = await lvl3frame.$( 'select[name^="TT3"]' );
		for (let chapt of await chaptsel.$$( 'option' )) {
			let avframe = page.frames( )[0].childFrames( )[0];
			let hrefs = await avframe.$$eval( 'a[href^="javascript:ci"]' ,
				links => links.map( link => link.href ));
			console.log( hrefs.length );
			chaptsel.press( 'ArrowDown' );
			chaptsel.press( 'Enter' );
			let submit = await lvl3frame.$( 'input[value^="lookup"]' );
			await submit.click( );
			await page.waitForNavigation( );
		}
		booksel.press( 'ArrowDown' );
		booksel.press( 'Enter' );
	}
})( );
