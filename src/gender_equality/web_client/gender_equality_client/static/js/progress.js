$(window).on('load', function(){
	const urlParams = new URLSearchParams(window.location.search);
	const detectorId = urlParams.get('detector_id');
	console.log(`ID: ${detectorId}`)
	const statusUrl = `http://localhost:5000/v1/gender_equality/${detectorId}/status`
	intervalLoop = setInterval(() => 
	{
		$.get(statusUrl, function(msg, status){
			//console.log(`DATA: ${msg}`)
			// console.log(`status: ${msg["data"]["status"]}`)
			// console.log(`percentage: ${msg["data"]["percentage"]}`)
			const progress = Math.floor(msg["data"]["percentage"]);
			$('#progressBar').attr('aria-valuenow', progress).css('width', progress + '%').text(progress + '%');
			if(progress == 100){
				clearInterval(intervalLoop);
				window.location.href = `/results?detector_id=${detectorId}`
			}
		})
	}, 5000);
})