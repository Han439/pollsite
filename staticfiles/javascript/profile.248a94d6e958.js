let close = $(".close-poll")

close.click(function(e) {
	$(this).html("CLOSED").addClass("closed")
	let questionId = $(this).parents(".poll-container").data("poll-id")
	console.log(questionId)
	$.ajax({
	    type:"put",
	    url: `/api/poll-question/${questionId}/`,
	    dataType:'json',
	    headers: {
			'Content-type': 'application/json',
			'X-CSRFToken': Cookies.get('csrftoken'),
			'Accept': 'application/json; indent=4',
		},
	    data: JSON.stringify({close: true}),
	    success: function(response) {
	        console.log(response);
	    }
	})
})

let del = $(".delete")
del.click(function(e) {
	let poll = $(this).closest(".poll-container")
	poll.fadeOut(500)
	let questionId = $(this).parents(".poll-container").data("poll-id")
	$.ajax({
	    type:"delete",
	    url: `/api/poll-question/${questionId}/`,
	    dataType:'json',
	    headers: {
			'Content-type': 'application/json',
			'X-CSRFToken': Cookies.get('csrftoken'),
			'Accept': 'application/json; indent=4',
		},
	    success: function(response) {
	        console.log(response);
	    }
	})
})
