const res = await fetch("http://0.0.0.0:4000/translate", {
	method: "POST",
	body: JSON.stringify({
		q: "hello",
		source: "en",
		target: "fr",
		format: "text",
		api_key: ""
	}),
	headers: { "Content-Type": "application/json" }
});

console.log(await res.json());